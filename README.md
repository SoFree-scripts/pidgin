# pidgin
Fun example of SoFplus communicating with Python to allow sending/receiving of messages while on the desktop.

Strings with 'http' in them are clickable.

Python checks the logfile for any new lines and pastes them into the tkinter text widget as they come.
SoFplus will print the string that you type into tkinter.

The window is renamed to 'Unread' if new messages come whilst the window is not in focus.
Also a sound can play on a new message

The im.exe was created with auto-py-to-exe and has the 'hitmarker.wav' included inside it.
(while in game, you wont hear it, only when SoF is minimised)

Plenty of improvements to be made as this is just a proof of concept-
*colours / SoF1 chars not handled
