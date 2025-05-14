inFp = None        # 입력 파일
inStr = ""         # 읽어 온 문자열

inFp = open("C:\\python\\data1.txt", "r", encoding="utf-8")

i = 1  # 행 번호 시작
while True:
    inStr = inFp.readline()
    if inStr == "":
        break
    print("%d: %s" % (i, inStr), end="")
    i += 1

inFp.close()
