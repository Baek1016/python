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

inFp,outFp = None,None
outStr =""

inFp = open("FileForder/data1.txt","r")
outFp = open("FileForder/data4.txt","w")

inList = inFp.readlines()
for inStr in inLinst:
    outFp.writelines(inStr)

inFp.close()
outFp.close()
print("--정상적으로 파일에 씀-- ")
