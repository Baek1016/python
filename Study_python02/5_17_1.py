# #이중함수
# # 외부함수는 정상 내부함수는 호출할수가 없다.
# def outFunc(v1,v2):
#     def inFunc(num1,num2):
#         return num1 + num2
#     return inFunc(v1,v2)

# print(outFunc(1,2))

# lambda 함수
#  간단하게 한 줄로 작성하는 익명 함수
def hap(num1,num2):
    res = num1+num2
    return res

print(hap(1,2))

# lambda 매게변수 : 리턴값
hap2 = lambda num1,num2: num1+num2
print(hap2(10,20))


