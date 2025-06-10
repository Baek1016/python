from tkinter import*

window = Tk()

photo1 = PhotoImage(file="C:/python/FileForder/anything-else-shut-up.gif")
photo2 = PhotoImage(file="C:/python/FileForder/excuse-me-wtf.gif")
                   
label1 = Label(window,image=photo1)
label2 = Label(window,image=photo2)

label1.pack(side=LEFT)
label2.pack(side=RIGHT)

window.mainloop()