"""
A fillin for german qwertz keyboard.
"""


def main(keyboard):
    keyboard.insert_key(0, '^', keyboard.ui.number_row, tooltip='Circumflex Accent')
    # add those before the Backspace key
    for i, k in [(11, 'ß'), (12, '´')]:
        keyboard.insert_key(i, k, keyboard.ui.number_row)

    for l in 'qwertzuiopü+':
        keyboard.add_key(l, keyboard.ui.letter_row_top)

    for l in 'asdfghjklöä#':
        keyboard.add_key(l, keyboard.ui.letter_row_middle)
    keyboard.add_key('enter', keyboard.ui.letter_row_middle, label='Enter')

    for i, k in enumerate('<yxcvbnm,.-'):
        keyboard.insert_key(i + 1, k, keyboard.ui.letter_row_bottom)
