from tkinter import *
import os

# 현재 실행 중인 파일 경로 기준
base_dir = os.path.dirname(os.path.abspath(__file__))

# 이미지 리스트 (문제에서 요구한 "1.gif" 형식)
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

# 창 설정
window = Tk()
window.geometry("700x500")
window.title("사진 앨범 보기")

# 버튼과 이름 라벨
btnPrev = Button(window, text="<< 이전", command=clickPrev)
btnNext = Button(window, text="다음 >>", command=clickNext)

# ✅ 테두리 빨간 박스 형태의 파일명 라벨
nameLabel = Label(
    window,
    text=fnameList[0],
    font=("Arial", 12),
    highlightthickness=1,
    highlightbackground="red",
    padx=10,
    pady=2
)

# 이미지 초기화
photo = PhotoImage(file=os.path.join(base_dir, fnameList[0]))
pLabel = Label(window, image=photo)

# 배치
btnPrev.place(x=200, y=10)
nameLabel.place(x=320, y=13)
btnNext.place(x=440, y=10)
pLabel.place(x=15, y=50)

window.mainloop()
