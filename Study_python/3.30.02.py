###컴프리헨션
# numList = []
# for num in range(1, 6):
#     numList.append(num)
# print(numList)

# # 컴프리 헨션으로 작성
# numList=[num for num in range(1,6)] 
# print(numList)

# numList = [num for num in range(1,6) if num % 2 == 0]
# print(numList)

# #1~5의 제곱으로 구성도니 리스트를 컴프리헨션으로 출력
# numList = [num**2 for num in range(1,6)]
# print(numList)


# #1~20 숫자 중에서 3의 배수로만 리스트를 구성 컴프리헨션으로 출력
# numList1 = [num for num in range(1,21) if num % 3 == 0]
# print(numList1)

## 리스트 코드와 비교: 리스트는 대괄호 []로 묶고 문자열은 작은 따옴표로 묵어 출력
# aa= [10,20,30,40,50]
# print(aa[0])
# print(aa[1:3])
# print(aa[3:1])

# ss="파이썬만세"
# print(ss[0])
# print(ss[1:3])
# print(ss[3:1])

# aa=[10,20,30]+[40,50]
# print(aa)
# ss="파이썬"+"만세"
# print(ss)

# aa=[10,20,30]*3
# print(aa)
# ss="파이썬"*3
# print(ss)

# aa=[10,20,30]
# print(len(aa))
# ss="파이썬"
# print(len(ss))  

# #문자열의 모든 글자 뒤에 $를 붙여서 출력하는 코드
# ss="파이썬짱!"
# sslen = len(ss)
# # sslist = [ss[i]+'$' for i in range(0,sslen)]
# for i in range(0,sslen):
#     print(ss[i]+'$',end ='')
# # print(sslist)

##문자열을 입력받아 반대로 출력
# inStr, ourStr = "",""
# count, i = 0, 0
# inStr = input("문자열을 입력하세요:")

# count = len(inStr)

# for i in range(0, count):
#     ourStr += inStr[count-(i+1)]
# print("입력한 문자열의 반전: ", ourStr)
#print ("입력한 문자열의 반전: ", inStr[::-1])
#print("입력한 문자열의 반전: %s" % ourStr)

# #문자열 양옆에  []넣은 후 문자열 중간의 공백까지 삭제해 주는 코드

# inStr = "   한글 Python 프로그래밍    "
# ourStr = ""
# count = len(inStr)

# for i in range(0,count-1):
#     if inStr[i] != ' ':
#         ourStr += inStr[i]

# print("원래 문자열=> [%s]" % inStr)

# print("입력한 문자열=> [%s]" % ourStr)


# #문자열을 입력받아 그중 o를 $로 변경하는 문자열을 변경을 응용

# ss=input("입력 문자열 ==> ")
# sslen = len(ss)
# # for i in range (0, sslen):
# print(ss.replace('o', '$'), end = "")
#     # if ss[i] == 'o':
#     #     print("$", end = "")
#     # else:
#     #     print(ss[i], end = "")

# ss='python을 열심히 공부 중'
# print(ss.split())
# aa ='하나\n둘\n셋'
# print(aa.splitlines())

# bb = '%'
# print(bb.join(['대한민국','만세']))

#날짜(연/월/일)입력==> 2023/10/31
#입력한 말짜의 10년 후 --> 2033년 03월 26일

ss = input("날짜를 입력하세요(년년/월/일) : ")
ssList = (ss.split('/'))
print("10년후 ==>")
print(str(int(ssList[0])+10)+"년",end=" ")
print(ssList[1]+"월",end=" ")
print(ssList[2]+"일",end=" ")
# for i in range (0,len(date)):
#     if i ==0:
#         aa='년'
#         print(aa.join(date[i]))
#     if i ==1:
#         bb='월'
#         print(bb.join(date[i]))
#     if i ==2:
#         cc='일'
#         print(cc.join(date[i]))