##윈도우 프로그래밍
# from tkinter import *

# window = Tk()

# window.mainloop()

# #윈도창 조절
# from tkinter import*
# window =Tk()
# window.tile("윈도우창 연습")
# window.geometry("400X100")
# window.resizavle(width =True, height =FALSE)#가로 크기 변경 가능하고 세로의 크기가 변경되지 않도록 지정
# window.mainloop()

# #레이블: 문자를 표현할 수 있는 위젯

# from tkinter import*

# window = Tk()

# label1 = Label(window, text="Korea")
# label2 = Label(window, text="만세", font=("궁서체", 30), fg="blue")
# label3 = Label(window, text="만만세", bg="magenta", width=20, height=5, anchor=SE)#anchor="se"

# label1.pack()
# label2.pack()
# label3.pack()

# window.mainloop()


# from tkinter import *

# window = Tk()

# window.mainloop()

# photo = PhotoImage(file = "/workspaces/python/GIF/dog.gif")
# label =Label(window, image = photo)

# label.pack()

# window.main.loop()
# 


# from tkinter import *

# window = Tk()
# button1 =Button(window,text="파이썬 종료",fg = "red",command=quit)

# button1.pack()

# window.mainloop()

# #이미지 ㅂ튼을 누르면 간단한 메시지창이 나오는 코드
# from tkinter import *
# from tkinter import messagebox

# def myFunc():
#     messagebox.showinfo("강아지 버튼", "멍멍")

# window = Tk()
# photo = PhotoImage(file="/workspaces/python/GIF/dog.gif")
# button1=Button(window, image =photo, command=myFunc)

# button1.pack()

# window.mainloop()

# #채크버튼(checkbutton) : 켜고 끄는데 사용하는 위젯

# from tkinter import *
# from tkinter import messagebox

# def myFunc():
#     if chk.get()==0:
#         messagebox.showinfo("aaa","체크버튼이 꺼졌어요")
#     else:
#         messagebox.showinfo("aaa","체크 버튼이 켜졌어요.")

# window = Tk()
# chk= IntVar()

# cb1 = Checkbutton(window,text="클릭하세요",variable= chk,command=myFunc)
# cb1.pack()

# window.mainloop()

# #라디오 버튼(radiobutton) : 여러 개 중에서 하나를 선택하는 데 사용하는 위젯
# from tkinter import*

# def myFunc():
#     if var.get ==1:
#         label1.configure(text="파이썬")
#     elif var.get ==2:
#         label1.configure(text="자바")
#     else:
#         label1.configure(text="c++")

# window = Tk()


# var = IntVar()

# rb1= Radiobutton(window,text="파이썬",variable=var, value =1, command = myFunc)
# rb2= Radiobutton(window,text="파이썬",variable=var, value =2, command = myFunc)
# rb3= Radiobutton(window,text="c++",variable=var, value =3, command = myFunc)

# label1=Label(window, text="선택한 언어: ", fg ="red")

# rb1.pack()
# rb2.pack()
# rb3.pack()

# window.mainloop()

# from tkinter import *

# window = Tk()

# button1 = Button(window, text = "버튼 1")
# button2 = Button(window, text = "버튼 2")
# button3 = Button(window, text = "버튼 3")

# button1.pack(side = LEFT)
# button2.pack(side = LEFT)
# button3.pack(side = LEFT)

# window.mainloop()

from tkinter import *

window = Tk()
btnList = [None]*3

for i in range(0,3):
    btnList[i]=Button(window, Text="버튼" + str(i+1))
for btn in btnList:
    btn.pack(side=TOP, fill=X)
    # btn.pack(side=LEFT)
    # btn.pack(side=RIGHT)
    # btn.pack(side=TOP)
    # btn.pack(side=BOTTOM,fill = X, ipadx = 10,ipady =10)
#여백을 조절하는데 위젯 내부의 여백 조절은 pad 
window.mainloop()