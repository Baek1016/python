from tkinter import *
import os

# 현재 파이썬 파일이 있는 폴더 기준으로 이미지 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))

# 전역 변수
fnameList = [
    "1.gif", "2.gif", "3.gif",
    "4.gif", "5.gif", "6.gif",
    "7.gif", "8.gif", "9.gif"
]
num = 0

def clickNext():
    global num
    num += 1
    if num > 8:
        num = 0
    photo = PhotoImage(file=os.path.join(base_dir, fnameList[num]))
    pLabel.configure(image=photo)
    pLabel.image = photo
    nameLabel.config(text=fnameList[num])

def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = 8
    photo = PhotoImage(file=os.path.join(base_dir, fnameList[num]))
    pLabel.configure(image=photo)
    pLabel.image = photo
    nameLabel.config(text=fnameList[num])

window = Tk()
window.geometry("700x500")
window.title("사진 앨범 보기")

btnPrev = Button(window, text="<< 이전", command=clickPrev)
btnNext = Button(window, text="다음 >>", command=clickNext)

photo = PhotoImage(file=os.path.join(base_dir, fnameList[0]))
pLabel = Label(window, image=photo)

nameLabel = Label(window, text=fnameList[0], font=("Arial", 12), fg="red")

btnPrev.place(x=200, y=10)
nameLabel.place(x=310, y=15)
btnNext.place(x=450, y=10)
pLabel.place(x=15, y=50)

window.mainloop()
