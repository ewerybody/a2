import argparse
import os
import sys

import logging
logging.getLogger('').setLevel(logging.DEBUG)
logging.info('!')
logging.getLogger('siding.style').setLevel(logging.INFO)

# Now, the important bits. import siding and make an application.
import siding
app = siding.QSingleApplication(sys.argv)

print('app.already_running: %s' % app.already_running)

# Set our app details. This is important for loading the profile and
# therefore for checking if it's a single instance or not.

app.setOrganizationName("Stendec")
app.setApplicationName("Generic Editor")
app.setApplicationVersion("1")

# Now, load the profile. Then check that this is the only instance. If there's
# a previous instance, app.ensure_single() will raise a SystemExit exception
# and we'll stop now before anything strenuous can happen.
siding.profile.initialize(True)
if not sys.argv[1:]:
    app.ensure_single('--show')
else:
    app.ensure_single()

# Since we're here, we're the only application. Continue loading as normal.
# While we're at it, initialize some more of siding.
siding.style.initialize(True)
siding.plugins.initialize(True)

# At this point, let's stop for a moment and import our window.
import main_window

# While we're on the topic of single-instance applications, message passing
# is useful. Let's set that up.

global windows
windows = []

def got_a_message(argv):
    print('got_a_message argv: %s' % argv)
    if argv == '--show':
        for win in windows:
            print('win: %s' % win)
            win.showRaise()
        return
    
    # Let's make this a list of files.
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILE', nargs='*',
                        help='A file to open for editing')

    args = parser.parse_known_args(argv)[0]
    count = 0

    # Open a window for every file.
    for file in args.files:
        if not os.path.isfile(file):
            print 'Invalid file: %s' % file
            continue

        # Make a window.
        count += 1
        win = main_window.MainWindow()

        # Open the file.
        win.do_open(file)

        # Spruce up the editor.
        siding.style.apply_stylesheet(win.editor, 'editor.qss')

        # ... and show it.
        win.show()
        windows.append(win)

    return count

app.messageReceived.connect(got_a_message)

# Why don't we do that now with our own arguments?
if not got_a_message(sys.argv[1:]):
    # Open at least one window.
    win = main_window.MainWindow()
    win.show()
    windows.append(win)

# And start the application.
app.exec_()
