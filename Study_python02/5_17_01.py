# #이중함수
# # 외부함수는 정상 내부함수는 호출할수가 없다.
# def outFunc(v1,v2):
#     def inFunc(num1,num2):
#         return num1 + num2
#     return inFunc(v1,v2)

# print(outFunc(1,2))

# # lambda 함수
# #  간단하게 한 줄로 작성하는 익명 함수
# def hap(num1,num2):
#     res = num1+num2
#     return res

# print(hap(1,2))

# # lambda 매게변수 : 리턴값
# hap2 = lambda num1,num2: num1+num2
# print(hap2(10,20))

# hap3 = lambda num1=10, num2=20: num1+num2
# print(hap3())
# print(hap3(100,200))

# myList=[1,2,3,4,5]
# add10= lambda num : num+10
# myList=list(map(add10,myList))
# print(myList)

# a= list(map(int,input("숫자를 입력하세요").split()))

# ex=list(map(lambda x:x*2,a))
# print(ex)

# list1 = [1,2,3,4]
# list2 = [10,20,30,40]

# hapList = list(map(lambda n1,n2:n1+n2, list1, list2))
# print(hapList)

# print(list(map(lambda n1,n2:n1+n2, [1,2,3,4], [10,20,30,40])))

# list_a= list(range(-5,5))
# print(list_a)

# list_b=[]
# for i in list_a:
#     if i<0:
#         list_b.append(i)
# print(list_b)

# def plust(l):
#     list_c=[]
#     for i in l:
#         if i<0:
#             list_c.append(i)
#     return list_c

# list_a= list(range(-5,5))

# c=plust(list_a)
# print(c)

list_m= range(-5,5)
# print(list_m,type(list_m))
# list_p=list(filter(lambda x:x<0, list_m))
# print(list_p)

# #컴프리핸션
# list_c =[i for i in list_m if i<0]
# print(list_c)

# list_a = list(range(-5,5))
# list_b= [i**2 for i in list_a if i<0]
# print(list_b)

# list_c= [i for i in range(1,11) if i%2==0]
