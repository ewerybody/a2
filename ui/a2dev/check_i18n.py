import sys
import json
from pathlib import Path

A2_ROOT = Path(__file__).parent.parent.parent
MOJIBAKE_HINTS = '\u00c3', '\ufffd', '\u00c2'
CHK_MARK = '\u2714'
EX_MARK = '\u2716'


def main():
    errors = []
    i18n_files = {
        *A2_ROOT.rglob('*/i18n/*.json'),
        *A2_ROOT.rglob('*/i18n/*/*.json'),
    }
    print(f'Found {len(i18n_files)} files. Scanning ...')
    for path in sorted(i18n_files):
        print(f'  {path.relative_to(A2_ROOT)}')
        text = path.read_text(encoding='utf-8')
        for hint in MOJIBAKE_HINTS:
            if hint not in text:
                continue
            errors.append(f"{path}: possible encoding issue (found '{hint}')")
            break
        try:
            json.loads(text)
        except json.JSONDecodeError as e:
            errors.append(f'{path}: invalid JSON - {e}')

    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    print(f'{CHK_MARK} - All checked! Nothing found!')


if __name__ == '__main__':
    main()
