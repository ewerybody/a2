"""
Created on 13.09.2017

@author: eric
"""


def main(keyboard):
    keyboard.insert_key(0, '`', keyboard.ui.number_row, tooltip='Tick')

    for l in 'qwertyuiop':
        keyboard.add_key(l, keyboard.ui.letter_row_top)
    keyboard.add_key('[', keyboard.ui.letter_row_top)
    keyboard.add_key(']', keyboard.ui.letter_row_top)
    keyboard.add_key('\\', keyboard.ui.letter_row_top)
#    keyboard.add_key('bracket_open_key', '[', keyboard.ui.letter_row_top)
#    keyboard.add_key('bracket_close_key', ']', keyboard.ui.letter_row_top)
#    keyboard.add_key('backslash_key', '\\', keyboard.ui.letter_row_top)

    for l in 'asdfghjkl':
        keyboard.add_key(l, keyboard.ui.letter_row_middle)
    keyboard.add_key(';', keyboard.ui.letter_row_middle)
    keyboard.add_key("'", keyboard.ui.letter_row_middle)
    keyboard.add_key('Enter', keyboard.ui.letter_row_middle, label='Enter')
#    keyboard.add_key('semicolon_key', ';', keyboard.ui.letter_row_middle)
#    keyboard.add_key('quote_key', "'", keyboard.ui.letter_row_middle)
#    keyboard.add_key('return_key', "Enter", keyboard.ui.letter_row_middle)

    for i, k in enumerate('zxcvbnm'):
        keyboard.insert_key(i + 1, k, keyboard.ui.letter_row_bottom)
    # for i, l, name in [(8, ',', 'comma'), (9, '.', 'dot'), (10, '/', 'slash')]:
    for i, k in [(8, ','), (9, '.'), (10, '/')]:
        keyboard.insert_key(i, k, keyboard.ui.letter_row_bottom)
