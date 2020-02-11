import tkinter

master = Tk()
cWidth = 1920  
cHeight = 1080
w = Canvas(master,width=cWidth,height=cHeight)
w.pack()

playX = (cWidth/2) - 12.5
playY = (cHeight/2) - 12.5
direct = 90

w.create_rectangle(playX,playY,playX+25,playY+25,fill="black")
mainloop()