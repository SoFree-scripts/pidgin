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
messages.pack()




input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side="bottom", fill=X,expand=True)
scroll_y = Scrollbar(window, orient="vertical", command=messages.yview)
scroll_y.pack(side="right", expand=True, fill="y")

messages.configure(yscrollcommand=scroll_y.set)

sizeOrig = os.path.getsize(log)
with open("seekdata", "w") as f:
	f.write(str(sizeOrig))

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
					window.title("Unread")
					#beep=pygame.mixer.Sound("hitmarker.wav") #Loading File Into Mixer
					#beep.set_volume(0.02)
					#beep.play() #Playing It In The Whole Device
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
	window.title("SoF Console")
	input_get = input_field.get()
	#messages.insert(INSERT, '%s\n' % input_get)
	# label = Label(window, text=input_get)
	messages.see("end")

	#send the line to SoFplus
	with open(func, "w") as f:
		input_get = input_get.replace("\"", "'")
		say = "set msgString \"" + input_get + "\""
		f.write(say)
	input_user.set('')
	return "break"


frame = Frame(window)  # , width=300, height=300)
input_field.bind("<Return>", Enter_pressed)
frame.pack()

threading1 = threading.Thread(target=checkUpdateLoop)
threading1.daemon = True
threading1.start()

window.mainloop()
