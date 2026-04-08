import os
import re
import time
import subprocess
from pathlib import Path

import rich.progress

import a2util
import a2dev.dependency.inkscape

import PIL.Image

THEME_DIR = Path(__file__).parent.parent.parent.parent / 'theme'
SOURCE_DIR = THEME_DIR / '_source'
SOURCE_ICONS = SOURCE_DIR / 'icons'
TMP_DIR = Path(os.getenv('TEMP', '')) / '.a2_tmp_icons'
CHK_MARK = '\u2714'
EX_MARK = '\u2716'
TEXT_COLOR_REPLACE = '#f111f1'


def main(force=False):
    """
    collect icon SVGs
    for theme_name in themes:
      get text color
      get todo items
      export
    """
    t0 = time.perf_counter()

    inkscape_exe = a2dev.dependency.inkscape.get_path()
    if not inkscape_exe.is_file():
        raise RuntimeError('We need Inkscape for this!!')

    logos_todo = _assemble_logos(force)
    icons_todo = _assemble_icons(force)
    if not logos_todo and not icons_todo:
        print(f'{CHK_MARK} nothing to do!')
        return

    print('Starting up Inkscape shell ...', end='')
    ink_proc = subprocess.Popen(
        [inkscape_exe, '--shell'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
    )
    assert ink_proc.stdin is not None and ink_proc.stdout is not None
    _wait_for_inkscape(ink_proc)
    print(f'\b\b\b{CHK_MARK} {time.perf_counter() - t0:.2f}s')

    progress = rich.progress.Progress(
        '[progress.description]{task.description}',
        rich.progress.BarColumn(),
        rich.progress.TimeRemainingColumn(),
    )
    progress.start()

    task_id = progress.add_task('Generating logo icons', total=len(logos_todo))
    TMP_DIR.mkdir(exist_ok=True)
    _process_todos(logos_todo, ink_proc, progress, task_id)

    for theme_name, todos in icons_todo.items():
        task_id = progress.add_task(f'Generating {theme_name} icons', total=len(todos))
        _process_todos(todos, ink_proc, progress, task_id)

    progress.stop()
    ink_proc.stdin.write('quit\n')
    ink_proc.stdin.flush()
    ink_proc.wait()

    print(f'took {time.perf_counter() - t0:.2f}s all in all.')


def _wait_for_inkscape(ink_proc):
    buf = ''
    while True:
        char = ink_proc.stdout.read(1)
        buf += char
        if buf.endswith('> '):
            return


def make_ico(png_path, ico_path, sizes=(16, 24, 32, 48, 128)):
    sort_size = sorted(sizes, reverse=True)
    img = PIL.Image.open(png_path).convert('RGBA')
    img.save(ico_path, format='ICO', sizes=[(s, s) for s in sort_size])
    ico = PIL.Image.open(ico_path)
    new_sizes = ico.info['sizes']
    if not all((s, s) in new_sizes for s in sort_size):
        print(f'ERROR on {ico_path}!\n Found sizes: {new_sizes} expected: {sort_size}')


def _assemble_logos(force: bool) -> list[tuple[Path, Path]]:
    logos_todo: list[tuple[Path, Path]] = []
    for item in SOURCE_DIR.glob('*.svg'):
        target = THEME_DIR / f'{item.stem}.ico'
        if not force and target.is_file() and os.path.getmtime(item) < os.path.getmtime(target):
            continue
        logos_todo.append((item, target))
    return logos_todo


def _assemble_icons(force: bool) -> dict[str, list[tuple[Path, Path]]]:
    icons_todo = {}
    for theme_item in THEME_DIR.glob('*'):
        if not theme_item.is_dir() or theme_item.name.startswith('_'):
            continue

        theme_colors = theme_item / 'colors.json'
        text_color = ''
        if theme_colors.is_file():
            this_color = a2util.json_read(theme_colors).get('text', '')
            if re.match('[0-9A-F]{6}', this_color):
                text_color = f'#{this_color}'

        for item in SOURCE_ICONS.glob('*.svg'):
            target = THEME_DIR / theme_item.name / f'{item.stem}.ico'
            if (
                not force
                and target.is_file()
                and os.path.getmtime(item) < os.path.getmtime(target)
                and os.path.getmtime(theme_colors) < os.path.getmtime(target)
            ):
                continue

            if not text_color:
                icons_todo.setdefault(theme_item.name, []).append((item, target))
                continue

            svg_code = a2util.load_utf8(item)
            if TEXT_COLOR_REPLACE not in svg_code:
                icons_todo.setdefault(theme_item.name, []).append((item, target))
                continue
            tmp_svg = TMP_DIR / theme_item.name / item.name
            tmp_svg.parent.mkdir(exist_ok=True)
            tmp_svg.write_text(svg_code.replace(TEXT_COLOR_REPLACE, text_color))
            icons_todo.setdefault(theme_item.name, []).append((tmp_svg, target))

    return icons_todo


def _process_todos(
    todos: list[tuple[Path, Path]],
    ink_proc: subprocess.Popen,
    progress: rich.progress.Progress,
    task_id: rich.progress.TaskID,
) -> None:
    assert ink_proc.stdin is not None and ink_proc.stdout is not None
    if not todos:
        return
    todos[0][1].parent.mkdir(exist_ok=True)
    for source, target in todos:
        tmp_png = TMP_DIR / f'{source.stem}.png'
        cmd = (
            f'file-open:{source}; export-filename:{tmp_png}; export-width:128; export-type:png; export-do; file-close\n'
        )

        ink_proc.stdin.write(cmd)
        ink_proc.stdin.flush()
        _wait_for_inkscape(ink_proc)
        make_ico(tmp_png, target)
        progress.update(task_id, advance=1)


# def make_tmp_png(inkscape_exe, tmp_dir, source):
#     this_png = tmp_dir / f'{source.stem}.png'
#     subprocess.run(
#         [
#             inkscape_exe,
#             '--export-type=png',
#             '--export-width=128',
#             '--export-background-opacity=0',
#             f'--export-filename={this_png}',
#             source,
#         ],
#         check=True,
#     )
#     return this_png


if __name__ == '__main__':
    main(force=True)
