# def func1():
#     global a # 전역변수 a를 사용하겠다고 선언
#     a =10 # 지역변수 >> 전역변수
#     print("func1()에서 a의 값 %d" % a)

# def func2():
#     print("func2()에서 a의 값 %d" % a)

# a = 20 # 전역변수

# func1()
# func2()

# def func1():
#     result = 100
#     return result

# def func2():
#     print("반환값이 없는 함수 실행")

# hap = 0

# hap = func1() # func1()의 반환값을 hap에 저장
# print("func1()의 반환값 : %d" % hap)
# func2() # 반환값이 없는 함수 실행

# def func1(x):
#     x+=1
#     print("1증가 했습니다.")
#     return x

# def func2(x):
#     x+=1
#     print("1증가 했습니다.")

# a= 10 

# a= func1(a)
# print("func1()의 반환값 : %d" % a)

# func2(a)
# print("func2()의 반환값 : %d" % a)


# def multi(v1,v2):
#     retList = []
#     res1 = v1 +v2
#     res2 = v1 -v2
#     retList.append(res1)
#     retList.append(res2)
#     return retList

# myList= []
# hap, sub=(0,0)
# myList = multi(10,20)
# hap = myList[0]
# sub = myList[1]

# print("multi()돌려준값 ==> %d,%d" % (hap, sub))



#매게 변수의 개수를 지정해 전달하는 방법
# def para2_func(v1,v2):
#     result = 0
#     result = v1 + v2
#     return result

# def para3_func(v1,v2,v3):
#     result = 0
#     result = v1 + v2 + v3
#     return result

# hap = 0
# hap = para2_func(10,20)
# print("para2_func()의 반환값 : %d" % hap)
# hap = para3_func(10,20,30)
# print("para3_func()의 반환값 : %d" % hap)


# def para_func(v1=0,v2=0,v3=0):
#     result = 0
#     result = v1 + v2 + v3
#     return result

# hap = 0

# a=int(input("정수 입력 : "))
# b=int(input("정수 입력 : "))
# c=int(input("정수 입력 : "))

# hap = para_func(a,b,c)
# print("para3_func()의 반환값 : %d" % hap)

# def para_func(v1=0, v2=0, v3=0):
#     result = v1 + v2 + v3
#     return result

# def para_func(*para):
#     result = 0
#     for num in para:
#         result += num
#     return result

# hap = 0

# hap = para_func(10, 20, 30)  # 매개변수 개수에 상관없이 사용 가능
# print("para_func()의 반환값 : %d" % hap)

# hap = para_func(10, 20)  # 매개변수 개수에 상관없이 사용 가능
# print("para_func()의 반환값 : %d" % hap)


# # 리스트로 입력받기
# numbers = list(map(int, input("정수 3개를 입력하세요 (공백으로 구분): ").split()))

# # 리스트를 함수의 매개변수로 전달
# hap = para_func(*numbers)  # 리스트를 언패킹하여 전달
# print("para3_func()의 반환값 : %d" % hap)




# def para_func(v1=0, v2=0, v3=0):
#     result = v1 + v2 + v3
#     return result

# hap = 0

# # 입력받기: 공백으로 구분된 정수 3개를 입력받아 리스트로 변환
# numbers = list(map(int, input("정수 3개를 입력하세요 (공백으로 구분): ").split()))

# # 리스트를 언패킹하여 함수에 전달
# hap = para_func(*numbers)  # 리스트 언패킹
# print("리스트를 사용한 para_func()의 반환값 : %d" % hap)

# # 입력받기: 공백으로 구분된 정수 3개를 입력받아 튜플로 변환
# numbers_tuple = tuple(map(int, input("정수 3개를 입력하세요 (공백으로 구분): ").split()))

# # 튜플을 언패킹하여 함수에 전달
# hap = para_func(*numbers_tuple)  # 튜플 언패킹
# print("튜플을 사용한 para_func()의 반환값 : %d" % hap)

# # 입력받기: 시작값, 끝값, 증가값을 입력받아 range 객체 생성
# start, end, step = map(int, input("range의 시작, 끝, 증가값을 입력하세요 (공백으로 구분): ").split())
# numbers_range = range(start, end, step)

# # range 객체를 리스트로 변환 후 언패킹하여 함수에 전달
# hap = para_func(*list(numbers_range)[:3])  # range에서 최대 3개의 값만 사용
# print("range를 사용한 para_func()의 반환값 : %d" % hap)

# import math

# def tuple_func(*args):
#     # 가변 인자를 받아 합을 계산
#     result = sum(args)  # args는 튜플로 처리됨
#     print("함수 내부에서 받은 값 (튜플):", args)
#     return result


# # 입력받기: 튜플 형식으로 숫자를 입력받음
# numbers_tuple = tuple(map(int, input("정수 여러 개를 입력하세요 (공백으로 구분): ").split()))

# # 튜플을 언패킹하여 함수에 전달
# hap = tuple_func(*numbers_tuple)  # 튜플 언패킹
# print("tuple_func()의 반환값 : %d" % hap)




# #트와이스 =9,# 블랙핑크 = 8, # 방탄소년단 = 7, # 레드벨벳 = 6, # 아이즈원 = 5, # 에이핑크 = 4, # 소녀시대 = 3, # 원더걸스 = 2, # 핑클 = 1
# def dic_func(**para):
#     for k in para.keys():
#         print("%s : %d" % (k, para[k]))
#     return para

# dic_func(트와이스=9, 블랙핑크=8, 방탄소년단=7, 레드벨벳=6, 아이즈원=5, 에이핑크=4, 소녀시대=3, 원더걸스=2, 핑클=1)


#로또 번호 생성기
# import random  
# def lotto_num():
#     num= random.sample(range(1, 46), 6)  # 1부터 45까지의 숫자 중에서 6개를 랜덤으로 선택
#     return num


# print("로또 번호:", lotto_num())


import random

def lotto_func():
    # 로또 번호를 생성하는 함수
    lotto_numbers = random.randrange(1, 46)  # 1부터 45까지의 숫자 중에서 6개를 랜덤으로 선택
    return lotto_numbers

lotto=[]
num = 0

while True:
    a = lotto_func()

    # 중복된 번호가 없도록 체크    
    # if lotto.count(a) ==0:
    #     lotto.append(a)
    # if lotto.count(a) >=6:
    #     break
    if a not in lotto:
        lotto.append(a)
    
    if len(lotto) == 6:
        break

lotto.sort()  # 정렬    
print("로또 번호:", lotto)