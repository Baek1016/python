from tkinter import *

## 함수 선언 부분 ##
def loadImage(fname):
    global inImage, XSIZE, YSIZE
    fp = open(fname, 'rb')  # 바이너리 읽기 모드

    for i in range(0, XSIZE):
        tmpList = []
        for k in range(0, YSIZE):
            data = int(ord(fp.read(1)))  # 바이트 하나 읽고 숫자로
            tmpList.append(data)
        inImage.append(tmpList)

    fp.close()


def displayImage(image):
    global XSIZE, YSIZE
    rgbString = ""
    for i in range(0, XSIZE):
        tmpString = ""
        for k in range(0, YSIZE):
            data = image[i][k]
            tmpString += "#%02x%02x%02x " % (data, data, data)  # R=G=B → 회색
        rgbString += "{" + tmpString + "} "
    paper.put(rgbString)


## 전역 변수 선언 ##
window = None
canvas = None
XSIZE, YSIZE = 256, 256
inImage = []  # 2차원 리스트 형태의 이미지 메모리

## 메인 코드 부분 ##
window = Tk()
window.title("흑백 사진 보기")

canvas = Canvas(window, height=XSIZE, width=YSIZE)
paper = PhotoImage(width=XSIZE, height=YSIZE)
canvas.create_image((XSIZE / 2, YSIZE / 2), image=paper, state="normal")

# 파일에서 → 메모리
filename = 'C:\python\FileForder\Lenna.raw'  # 실제 파일 경로로 바꿔야 함
loadImage(filename)

# 메모리에서 → 화면
displayImage(inImage)

canvas.pack()
window.mainloop()
