from Tkinter import * 
from show_stuff import get_google_information, start_up, send_message
from time import sleep
from PIL import Image

def on_send():
	global root, frame3, frame2
	send_message()
	frame2.pack_forget()
	frame3.pack()#.grid(sticky=E+W+N)
	photo = PhotoImage(file="qr_code.png")
	label1 = Label(frame3, image=photo)
	label1.pack()
	sleep(30)
	#label1.pack_forget()
	frame3.pack_forget()
	frame2.pack()
	
	
def draw():
	global label1, root, frame2, frame3
	root.geometry("480x320") #800x480 12
	(message, color) = get_google_information()
	frame2 = Frame(root, border =6, relief = RAISED)
	frame2.pack(fill=BOTH, side=TOP)#.grid(sticky=E+W+N)
	frame3 = Frame(root, border =6, relief = RAISED)
	frame2.columnconfigure(0, weight=1)
	frame2.rowconfigure(0, weight=1)
	label1 = Label(frame2, text=message, bg = color, height = 7, wraplength=300, font = ("Helvetica", 16))
	label1.grid(rowspan=3, columnspan=3, sticky="nsew")
	button1 = Button(frame2, text = "Leave Message",  bg="teal", command= lambda: on_send())
	button1.grid(row=4, column=0)


def refresh():
	global label1, root, button	
	(message, color) = get_google_information()
	label1.configure(text=message, bg = color)
	root.after(20000, refresh)

	
def main():
	global root
	root = Tk()
	draw()
	refresh()
	root.mainloop()


if __name__ == '__main__':
	main() 

