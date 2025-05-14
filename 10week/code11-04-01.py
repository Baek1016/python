inFp = None
inList, inStr = [], ""

inFp = open("C:\\python\\data1.txt", "r", encoding="utf-8")

inList = inFp.readlines()

i = 1  # 줄 번호 초기화
for inStr in inList:
    print("%d: %s" % (i, inStr), end="")
    i += 1  # 줄 번호 증가

inFp.close()
