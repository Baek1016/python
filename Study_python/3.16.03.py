#생년월일 을 입력(birth)받아 만 나이를 계산하는 프로그램을 작성하시오.(단 오늘 날짜를 기분으로 혹은 내가 설정해서 계산하시오.)
#ex) 생년월일:2000.10.16  만 나이: 24세
from datetime import date

# birth = input("생년월일을 입력하세요(yyyy.mm.dd): ")
# year, month, day = map(int, birth.split('.'))
# print(year, month, day)

# today = date.today()
# print(today)    #2021-03-16 출력

# age = today.year - year
# if today.month < month or (today.month == month and today.day < day):
#     age -= 1
# print(f"생년월일: {birth} 만 나이: {age}세")


# birth = input("생년월일을 입력하세요(yyyy.mm.dd): ")

# fruit = ['사과','배','딸기','포드']
# print(fruit)
# fruit.append('귤')
# print(fruit)
# if '딸기' in fruit:
#     print("딸기가 있습니다.")
# if '수박' in fruit:
#     print("수박이 있습니다.")

# random.randrange(0,3) random.randrange()함수는 import random을 해야 사용가능하다.
import random

# print(random.randrange(0,3))

# for i in range(0,10,1):
#     print("%d" % i)

num =[]
# for i in range(0,5,1):
#     num.append(i)
# print(num)
# for i in range(0,5,1):
#     num.insert(0,i)
# print(num)

#for 문으로 난수(0~9)를 append()사용하여 num[]에 항목 5개 추가

# for i in range(0,5,1):
#     # print(f"{i+1}번")
#     num.append(random.randrange(0,10))
# print(num)

# if 0 in num:
#     print("0 있음")
# if 1 in num:
#     print("1 있음")
# if 2 in num:
#     print("2 있음")
# if 3 in num:
#     print("3 있음")
# if 4 in num:
#     print("4 있음")
# if 5 in num:
#     print("5 있음")
# if 6 in num:
#     print("6 있음")
# if 7 in num:
#     print("7 있음")
# if 8 in num:
#     print("8 있음")
# if 9 in num:
#     print("9 있음")

#for문으로 난수(0~9)를 append()사용하여 num[]에 항목 5개 추가 if~in을 사용하세오.

for i in range(0,5,1):
    num.append(random.randrange(0,10))
print(num)

for i in range(0,10,1):
    if i in num:
        print(f"{i} 있음")
    else:
        print(f"{i} 없음")