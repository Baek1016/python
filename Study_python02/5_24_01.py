# outFp =None
# outStr = ""

# outFp = opem("FileForder/data1.txt","w")

# while True :
#     outStr = input("내용 입력: ")
#     if outStr != "":
#         outFp.Wrtielines(outStr + "\n")

#     else:
#         break
    
# outFp.close()
# print("--정상적으로 파일에 씀-- ")

##data1.txt을 data4.txt에다가 복사 

# inFp,outFp = None,None
# outStr =""
# secuYN = input("1.암호화 2.암호 해석 : ")
# inFname = input("입력 파일명을 입력하세요 : ")
# outFname = input("출력 파일명을 입력하세요 : ")
# # inFp = open("FileForder/data1.txt","r")
# # outFp = open("FileForder/data4.txt","w")

# # inList = inFp.readlines()
# # for inStr in inList:
# #     outFp.writelines(inStr)

# # inFp.close()
# # outFp.close()
# # print("--정상적으로 파일에 씀-- ")

# if secuYN == "1":
#     secu = 100
# elif secuYN == "2":
#     secu = -100
# else:
#     print("잘못된 입력입니다.")
#     exit()

# inFp = open(inFname,'r', encoding = 'utf-8')
# outFp = open(inFname,'w', encoding = 'utf-8')

# while True:
#     inStr = inFp.readlines()
#     if not inStr:
#         break

#     outStr = ""

#     for i in range(0,len(inStr)):
#         ch = inStr[i]
#         chNum = ord(ch)#문자를 숫자로 바꾸는 함수
#         chNum = chNum + secu
#         ch2 = chr(chNum)
#         outStr= outStr + ch2
#     outFp.write(outStr)

# outFp.close()
# inFp.close()
# print("%s ==> %s 변환완료" % (inFname, outFname))

# inFp,outFp = None,None
# inStr,outStr
# i =0
# secu = 0

# if secuYn = input("1.암호화 2. 암호화해석")
# inFname = input("입력 파일명을 입력하세요 : ")
# outFname = input("입력 파일명을 입력하세요 : ")

# while True:
#     instr = inFp.res

#encoding textFile
# ...existing code...

secuYN = input("1.암호화 2.암호 해석 : ")
inFname = input("입력 파일명을 입력하세요 : ")
outFname = input("출력 파일명을 입력하세요 : ")

if secuYN == "1":
    secu = 100
elif secuYN == "2":
    secu = -100
else:
    print("잘못된 입력입니다.")
    exit()

inFp = open(inFname, 'r', encoding='utf-8')
outFp = open(outFname, 'w', encoding='utf-8')

inList = inFp.readlines()
for inStr in inList:
    outStr = ""
    for ch in inStr:
        chNum = ord(ch)
        chNum = chNum + secu
        ch2 = chr(chNum)
        outStr = outStr + ch2
    outFp.write(outStr)

outFp.close()
inFp.close()
print("%s ==> %s 변환완료" % (inFname, outFname))
# ...existing code...