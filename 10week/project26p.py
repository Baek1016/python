outFp = None
outStr = ""
fName = input("저장할 파일명을 입력하세요 : ")

outFp = open(fName, "w", encoding="utf-8")

while True:
    outStr = input("내용 입력 : ")
    if outStr != "":
        outFp.write(outStr + "\n")
    else:
        break

outFp.close()
print("--- 정상적으로 파일에 씀 ---")
