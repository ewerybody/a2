"""
Fillin for en english qwerty keyboard.
"""


def main(keyboard):
    keyboard.insert_key(0, '`', keyboard.ui.number_row, tooltip='Tick')
    # add those before the Backspace key
    for i, k in [(11, '-'), (12, '=')]:
        keyboard.insert_key(i, k, keyboard.ui.number_row)

    for l in 'qwertyuiop':
        keyboard.add_key(l, keyboard.ui.letter_row_top)
    keyboard.add_key('[', keyboard.ui.letter_row_top)
    keyboard.add_key(']', keyboard.ui.letter_row_top)
    keyboard.add_key('\\', keyboard.ui.letter_row_top)

    for l in 'asdfghjkl':
        keyboard.add_key(l, keyboard.ui.letter_row_middle)
    keyboard.add_key(';', keyboard.ui.letter_row_middle)
    keyboard.add_key("'", keyboard.ui.letter_row_middle)
    keyboard.add_key('enter', keyboard.ui.letter_row_middle, label='Enter')

    for i, k in enumerate('zxcvbnm'):
        keyboard.insert_key(i + 1, k, keyboard.ui.letter_row_bottom)
    for i, k in [(8, ','), (9, '.'), (10, '/')]:
        keyboard.insert_key(i, k, keyboard.ui.letter_row_bottom)
