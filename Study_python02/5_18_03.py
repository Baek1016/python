# #파일 입출력
# inFp = None#파일인데 아무것도 없다.
# inStr = "" #문자인데 아무것도 없다.

# inFp = open("./123.txt","r",encoding="utf-8")

# inStr = inFp.readline()
# print(inStr,end = "")

# inStr = inFp.readline()
# print(inStr,end = "")

# inStr = inFp.readline()
# print(inStr,end = "")

# inFp.close()

# #파일 입출력
# inFp = None#파일인데 아무것도 없다.
# inStr = "" #문자인데 아무것도 없다.

# inFp = open("./123.txt","r",encoding="utf-8")

# while True:
#     inStr = inFp.readline()
#     if inStr == "":
#         break
#     print(inStr,end = "")

# inFp.close()

# inFp = None#파일인데 아무것도 없다.
# inList = "" #문자인데 아무것도 없다.

# inFp = open("./123.txt","r",encoding="utf-8")

# inList = inFp.readlines()
# print(inList,end = "")

# inFp.close()
import os

inFp = None#파일인데 아무것도 없다.
fName = "" #파일이름
inStr = "" #문자인데 아무것도 없다.
inList = [] #리스트인데 아무것도 없다.

fName = input("읽어올 파일 이름을 입력하세요 : ")
if os.path.exists(fName) == False:
    inFp = open(fName,"r")

    inList = inFp.readlines()
    for inStr in inList:
        print(inStr,end = "")

    inFp.close()

else:
    print("파일이 존재하지 않습니다.")
    inFp = open(fName,"w",encoding="utf-8")
    inStr = input("파일에 저장할 내용을 입력하세요 : ")
    inFp.write(inStr)
    inFp.close()