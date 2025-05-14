outFp = None
outStr = ""

outFp = open("C:\python\FileForder\data2.txt", "w", encoding="utf-8")

while True:
    outStr = input("내용 입력 : ")
    if outStr != "":
        outFp.write(outStr + "\n")  # ← writelines 대신 write를 추천
    else:
        break

outFp.close()
print("--- 정상적으로 파일에 씀 ---")
