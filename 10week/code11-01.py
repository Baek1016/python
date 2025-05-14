inFp = None        # 입력 파일
inStr = ""         # 읽어 온 문자열

inFp = open("C:\\python\\data1.txt", "r", encoding="utf-8")


inStr = inFp.readline()
print(inStr, end = "")

inStr = inFp.readline()
print(inStr, end = "")

inStr = inFp.readline()
print(inStr, end = "")

inFp.close()
