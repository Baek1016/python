inFp, outFp = None, None
inStr, outStr = "", ""
secu = 0

print("1. 암호화  2. 암호 해석 중 선택 : ", end="")
choice = int(input())

if choice == 1:
    secu = 100
elif choice == 2:
    secu = -100
else:
    print("잘못 입력하였습니다.")
    exit()

inName = input("입력 파일명을 입력하세요 : ")
outName = input("출력 파일명을 입력하세요 : ")

inFp = open(inName, "r", encoding="utf-8")
outFp = open(outName, "w", encoding="utf-8")

while True:
    inStr = inFp.readline()
    if not inStr:
        break

    outStr = ""
    for ch in inStr:
        outStr += chr(ord(ch) + secu)
    outFp.write(outStr)

inFp.close()
outFp.close()

print(f"{inName} --> {outName} 변환 완료")
