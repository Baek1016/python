from tkinter import *
import os
import random  # 🔹 shuffle을 위한 모듈

## 전역 변수 선언 부분 ##
btnList = [None] * 9
fnameList = [
    "1.gif", "2.gif", "3.gif",
    "4.gif", "5.gif", "6.gif",
    "7.gif", "8.gif", "9.gif"
]
photoList = [None] * 9
i, k = 0, 0
xPos, yPos = 0, 0
num = 0

# 🔹 리스트 순서 무작위로 섞기
random.shuffle(fnameList)

## 메인 코드 부분 ##
window = Tk()
window.geometry("210x210")

# 이미지 경로 설정
img_dir = "C:/python/09week"  # 슬래시(/) 또는 역슬래시(\\) 잘 써야 함

for i in range(9):
    full_path = os.path.join(img_dir, fnameList[i])  # 안전하게 경로 조합
    photoList[i] = PhotoImage(file=full_path)
    btnList[i] = Button(window, image=photoList[i])

for i in range(3):
    for k in range(3):
        btnList[num].place(x=xPos, y=yPos)
        num += 1
        xPos += 70
    xPos = 0
    yPos += 70

window.mainloop()
