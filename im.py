from tkinter import *

import os
import time
import threading 
import webbrowser
#import pygame
log = "C:\\Users\\Human\\Desktop\\Raven\\SOF PLATINUM\\user\\sof.log"
func = "C:\\Users\\Human\\Desktop\\Raven\\SOF PLATINUM\\user\\sofplus\\data\\pidgin.cfg"

window = Tk()

messages = Text(window)
messages.pack()

scroll_y = Scrollbar(window, orient="vertical", command=messages.yview)
scroll_y.pack(side="left", expand=True, fill="y")

messages.configure(yscrollcommand=scroll_y.set)


input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)

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
			with open(log, "r") as f:
				f.seek(int(oldsize))
				line = f.readlines()
			for x in line:
				#print all lines to widget
				if ": [" in x:
					insertMe = ""
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
					#pygame.mixer.music.load("pop.mp3") #Loading File Into Mixer
    				#pygame.mixer.music.play() #Playing It In The Whole Device
					if float(scroll_y.get()[1]) > 0.9:
						messages.see("end")
		time.sleep(1)

def urlClick(e,url):
	print(url)
	webbrowser.open_new(url)

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
    input_get = input_field.get()
    messages.insert(INSERT, '%s\n' % input_get)
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