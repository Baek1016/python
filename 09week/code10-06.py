from tkinter import*
from tkinter import messagebox

def myFunc():
    messagebox.showinfo("강아지 버튼", "강아지가 귀엽죠? ^^")


window = Tk()

photo = PhotoImage(file="C:/python/FileForder/005380.KS_candle.png")
button1 = Button(window, image= photo,command= myFunc)

button1.pack()

window.mainloop()