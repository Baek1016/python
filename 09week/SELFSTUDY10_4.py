from tkinter import *
from tkinter import messagebox

# 이벤트 함수 정의
def keyEvent(event):
    key_name = ""

    # 방향키 구분
    if event.keycode == 37:
        key_name = "왼쪽 화살표"
    elif event.keycode == 38:
        key_name = "위쪽 화살표"
    elif event.keycode == 39:
        key_name = "오른쪽 화살표"
    elif event.keycode == 40:
        key_name = "아래쪽 화살표"
    else:
        key_name = chr(event.keycode)

    # Shift 키 감지 (비트 연산으로 확인)
    if event.state & 0x0001:
        key_name = "Shift + " + key_name

    # 메시지 출력
    messagebox.showinfo("키보드 이벤트", "눌린 키 : " + key_name)

# 창 설정
window = Tk()
window.bind("<Key>", keyEvent)
window.mainloop()
