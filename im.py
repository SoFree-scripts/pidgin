from tkinter import *

import os
import time
import threading 
import webbrowser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from win32 import win32gui
import re


log = os.path.join(".","sof.log")
func = os.path.join(".","sofplus/data/pidgin.cfg")
desktop = os.path.join(".","sofplus/data/pidgin_desktop.cfg")
mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
mixer.init()

window = Tk()

window.title("SoF Console")
messages = Text(window)
messages.configure(state="disable",wrap=WORD,bg="black",fg="white")





input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.configure(bg="grey",fg="white")
scroll_y = Scrollbar(window, orient="vertical", command=messages.yview)
scroll_y.configure(bg="black")
scroll_y.pack(side="right",fill="y")
input_field.pack(side="bottom", fill="x")
input_field.focus_set()
messages.pack(side="bottom")


messages.configure(yscrollcommand=scroll_y.set)

sizeOrig = os.path.getsize(log)
with open("seekdata", "w") as f:
	f.write(str(sizeOrig))

mySlot = "@"
winId = ""
sofId = ""

def checkUpdateLoop():
	global winId
	global sofId
	nameSet = 0
	nameRem = 0
	while True:
		#get winId
		if winId == "":
			#remove 'unread' title when window is maximised (ideally this would be some kind of hook)
			win32gui.EnumWindows( winEnumHandler, None )
		if sofId == "":
			win32gui.EnumWindows( sofWinEnumHandler, None )
		else:
			#sof.exe open
			if win32gui.GetForegroundWindow() != sofId:
				with open(desktop, "r+") as f:
					f.seek(0)
					f.write("                                 \n")
					f.write("                                 \n")
					f.seek(0)
					f.write("//desktop namehello    \n")
					f.write("set ~desktop \"1\"       \n")
			else:
				with open(desktop, "r+") as f:
					f.seek(0)
					f.write("                                 \n")
					f.write("                                 \n")
					f.seek(0)
					f.write("//desktop name12334   \n")
					f.write("set ~desktop \"\"        \n")
		with open("seekdata", "r") as f:
			line = f.readlines()
		oldsize = line[0].replace("\n","")
		fsize = os.path.getsize(log)
		#print fzize
		#print oldsize
		if int(oldsize) < fsize:
			with open("seekdata", "w") as f:
				f.write(str(fsize))
			with open(log, "r",encoding="latin-1") as f:
				f.seek(int(oldsize))
				line = f.readlines()
			for x in line:
				#print all lines to widget
				if ": [" in x:
					#a chat message
					insertMe = ""
					messages.configure(state="normal")
					#set name colour
					x = setNameColour(x)
					for s in x.split():
						if "http" not in s:
							insertMe += (str(s) + " ")
							#print insertMe
						else:
							#print text before http
							messages.insert(END, '%s' % insertMe)
							#handle the url
							urlHandler(s)
							#reset string
							insertMe = " "
					insertMe += "\n"
					messages.tag_config("text", foreground=_from_rgb((204,204,204)))
					messages.insert(END, insertMe, "text")
					#print(mySlot)
					if mySlot not in x:
						#if its not our own input, no beep
						window.title("Unread")
						beep=mixer.Sound(resource_path("hitmarker.wav")) #Loading File Into Mixer
						beep.set_volume(0.02)
						beep.play() #Playing It In The Whole Device
					if float(scroll_y.get()[1]) > 0.9:
						messages.see("end")
					messages.configure(state="disable")
		if win32gui.GetForegroundWindow() == winId:
			window.title("SoF Console")
		time.sleep(1)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

def setNameColour(x):
	m = re.split(": \[\d{1,2}\]",x)
	name = m[0]
	messages.tag_config("name", foreground=_from_rgb((37,188,36)))
	messages.tag_config("name",font=("Georgia", "11", "bold"))
	messages.insert(END, name, "name")
	#client slot important
	lname = len(m[0])
	return x[lname:]
	


def winEnumHandler( hwnd, ctx ):
	global winId
	#if win32gui.IsWindowVisible( hwnd ):
	#print (hex(hwnd), win32gui.GetWindowText( hwnd ))
	if win32gui.GetWindowText( hwnd ) == "SoF Console":
		winId = hwnd

def sofWinEnumHandler( hwnd, ctx ):
	global sofId
	#if win32gui.IsWindowVisible( hwnd ):
	#print (hex(hwnd), win32gui.GetWindowText( hwnd ))
	if win32gui.GetWindowText( hwnd ) == "SoF":
		sofId = hwnd

def urlHandler(url):
	#we have a httplink
	#print messages before
	messages.tag_config("tag1", foreground="blue", background="green")
	messages.tag_bind("tag1", "<Button-1>", lambda e:callback(e, url))
	messages.insert(END, url, "tag1")

def callback(event, tag):
	webbrowser.open_new(tag)
    #print(event.widget.get('%s.first'%tag, '%s.last'%tag))

def Enter_pressed(event):
	global mySlot
	window.title("SoF Console")
	input_get = input_field.get()
	if input_get != "":
		ourLastMsg = input_get
		#messages.insert(INSERT, '%s\n' % input_get)
		# label = Label(window, text=input_get)
		messages.see("end")

		#send the line to SoFplus
		#// cvar: pidgin.cfg msgString 0
		#set "msgString" ""
		#set "~slot" ""
		with open(func, "r+") as f:
			line = f.readlines()
			#print(line)
			if "String" in line[2]:
				tmp = line[1]
				line[1] = line[2]
				line[2] = tmp
			mySlot = line[2].split()
			#print(mySlot)
			num = mySlot[2].replace("\"","")
			mySlot = ": [" + str(num) + "] "
			input_get = input_get.replace("\"", "'")
			line1 = "set msgString \"" + input_get + "\"\n"
			line2 = "set ~slot \"" + str(num) + "\""
			#print("line2 =:" + line2)
			f.seek(0)
			f.write("                                 \n")
			f.write("                                 \n")
			f.write("                                 \n")
			f.seek(0)
			f.write("//Sssome cvars\n")
			f.write(line1)
			f.write(line2)
		input_user.set('')
	return "break"


frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()

threading1 = threading.Thread(target=checkUpdateLoop)
threading1.daemon = True
threading1.start()

window.mainloop()
