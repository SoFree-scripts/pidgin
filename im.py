from tkinter import *

import os
import time
import threading 
import webbrowser
#os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
#import pygame
log = os.path.join(".","sof.log")
func = os.path.join(".","sofplus/data/pidgin.cfg")
#pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
#pygame.mixer.init()

window = Tk()
window.title("SoF console")
messages = Text(window)
messages.configure(state="disable",wrap=WORD)





input_user = StringVar()
input_field = Entry(window, text=input_user)
scroll_y = Scrollbar(window, orient="vertical", command=messages.yview)
scroll_y.pack(side="right",fill="y")
input_field.pack(side="bottom", fill="x")
input_field.focus_set()
messages.pack(side="bottom")


messages.configure(yscrollcommand=scroll_y.set)

sizeOrig = os.path.getsize(log)
with open("seekdata", "w") as f:
	f.write(str(sizeOrig))

mySlot = "@"

def checkUpdateLoop():
	while True:
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
					messages.insert(END, '%s' % insertMe)
					if mySlot not in x:
						#if its not our own input, no beep
						window.title("Unread")
						#beep=pygame.mixer.Sound("hitmarker.wav") #Loading File Into Mixer
						#beep.set_volume(0.02)
						#beep.play() #Playing It In The Whole Device
					else:
						print("no need to beep us right?")
					if float(scroll_y.get()[1]) > 0.9:
						messages.see("end")
					messages.configure(state="disable")
		time.sleep(1)

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
		print(line)
		if "String" in line[2]:
			tmp = line[1]
			line[1] = line[2]
			line[2] = tmp
		mySlot = line[2].split()
		num = mySlot[2].replace("\"","")
		mySlot = ": [" + str(num) + "] "
		input_get = input_get.replace("\"", "'")
		line1 = "set msgString \"" + input_get + "\"\n"
		line2 = "set ~slot \"" + str(num) + "\""
		f.seek(0)
		f.write("//Sssome cvars\n")
		#this is what a headache looks like
		f.write("                                 ")
		f.write("                                 ")
		f.seek(0)
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
