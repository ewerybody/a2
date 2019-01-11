# -*- coding: utf-8 -*-
"""
A fillin for german qwertz keyboard.
"""


def main(keyboard):
    keyboard.insert_key(0, '^', keyboard.ui.number_row, tooltip='Circumflex Accent')
    # add those before the Backspace key
    # if we don't give a label it will try uppercase ß to SS :|
    for i, key, label, in [(11, 'ß', 'ß'), (12, '´', None)]:
        keyboard.insert_key(i, key, keyboard.ui.number_row, label)

    for l in 'qwertzuiopü+':
        keyboard.add_key(l, keyboard.ui.letter_row_top)

    for l in 'asdfghjklöä#':
        keyboard.add_key(l, keyboard.ui.letter_row_middle)
    keyboard.add_key('enter', keyboard.ui.letter_row_middle, label='Enter')

    for i, k in enumerate('<yxcvbnm,.-'):
        keyboard.insert_key(i + 1, k, keyboard.ui.letter_row_bottom)
