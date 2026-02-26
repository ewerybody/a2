#!/usr/bin/env python3
"""Run AHKUnit-compatible *.test.ahk files from the command line.

Generates a minimal temp script per test file, runs it with the bundled
AutoHotkey interpreter, and reports results. Exit code 0 = all pass.
"""

import re
import sys
import subprocess
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
AHK_EXE = SCRIPT_DIR.parent.parent / 'AutoHotkey.exe'
RUNNER_LIB = SCRIPT_DIR / 'a2test.ahk'
INDENTATION = ' '

# Tree node type: {'methods': [str, ...], 'children': {str: node}}
TestNode = dict


def parse_test_structure(source: str) -> TestNode:
    """Parse a .test.ahk source into a nested tree.

    Returns: {'ClassName': {'methods': [...], 'children': {'Sub': ...}}}
    Uses brace-depth tracking — indentation-independent.
    Methods starting with _ are skipped (AHKUnit convention).
    """
    root: TestNode = {}
    # stack entries: (name, entry_depth, node)
    class_stack: list[tuple[str, int, TestNode]] = []
    depth = 0

    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(';') or stripped.startswith('#'):
            continue

        # Pop classes we've left since the last line
        while class_stack and class_stack[-1][1] > depth:
            class_stack.pop()

        opens = stripped.count('{')
        closes = stripped.count('}')

        # Class declaration: starts with "class Name"
        m = re.match(r'class\s+(\w+)', stripped, re.IGNORECASE)
        if m:
            cls_name = m.group(1)
            depth += opens - closes  # normally +1
            node: TestNode = {'methods': [], 'children': {}}
            parent = class_stack[-1][2]['children'] if class_stack else root
            parent[cls_name] = node
            class_stack.append((cls_name, depth, node))
            continue

        # Method: starts with "name()" and we're at the class body level
        if class_stack and class_stack[-1][1] == depth:
            m = re.match(r'(\w+)\s*\(\s*\)', stripped)
            if m and not m.group(1).startswith('_'):
                class_stack[-1][2]['methods'].append(m.group(1))

        depth += opens - closes

    return root


def _generate_calls(tree: TestNode, ahk_prefix: str, level: int) -> list[str]:
    """Recursively generate A2TestClass + A2Test AHK call lines."""
    lines = []
    indent = INDENTATION * level
    method_indent = INDENTATION * (level + 1)
    for cls_name, node in tree.items():
        ahk_path = f'{ahk_prefix}.{cls_name}' if ahk_prefix else cls_name
        lines.append(f'A2TestClass("{cls_name}", "{indent}")')
        for method in node['methods']:
            lines.append(
                f'_failures += A2Test("{method}", () => {ahk_path}().{method}(), "{method_indent}")'
            )
        lines.extend(_generate_calls(node['children'], ahk_path, level + 1))
    return lines


def run_test_file(test_file: Path) -> int:
    """Generate + run a temp script for one .test.ahk file.
    Returns number of files with failures (0 or 1)."""
    source = test_file.read_text(encoding='utf-8')
    tree = parse_test_structure(source)
    if not tree:
        print('  (no test classes found, skipping)')
        return 0

    calls = _generate_calls(tree, '', 0)
    script = (
        '#Requires AutoHotkey v2.0\n'
        '#NoTrayIcon\n'
        '#ErrorStdOut "UTF-8"\n'
        f'#Include "{RUNNER_LIB}"\n'
        f'#Include "{test_file}"\n'
        '_failures := 0\n'
        + '\n'.join(calls) + '\n'
        'ExitApp(_failures > 0 ? 1 : 0)\n'
    )

    with tempfile.NamedTemporaryFile(
        suffix='.ahk', mode='w', encoding='utf-8', delete=False
    ) as file_obj:
        tmp = Path(file_obj.name)
        file_obj.write(script)

    try:
        exitcode, result = subprocess.getstatusoutput([AHK_EXE, tmp], encoding='utf-8')
        if result:
            print(result)
        return 0 if exitcode == 0 else 1
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    if not AHK_EXE.exists():
        print(f'AutoHotkey not found: {AHK_EXE}', file=sys.stderr)
        return 1

    test_files = sorted(SCRIPT_DIR.glob('*.test.ahk'))
    if not test_files:
        print('No *.test.ahk files found.')
        return 0

    failed = 0
    for test_file in test_files:
        print(f'\n=== {test_file.name} ===')
        failed += run_test_file(test_file)

    if failed:
        print(f'FAILED ({failed} file(s) with errors)')
    else:
        print(f'All {len(test_files)} AHK tests passed!')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
