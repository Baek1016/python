#사용자에게 0부터 100사이의 하나의 수를 입력받아 3,6,9가 들어있으면 "crap"를 출력하고
#그렇지 않으면 "next number"로 출력하는 사용자 정의 함수(game)

# def game(a):
#     if int(a) <0 or int(a)>100:
#         print("0부터 100사이의 수를 입력하세요")
#     elif '3' in a or '6' in a or '9' in a:
#         print("crap")
#     else:
#         print("next number")

# def game(num):
#     a= num//10
#     b= num%10

#     if a==3 or a==6 or a==9:
#         print("crap")
#     elif b==3 or b==6 or b==9:
#         print("crap")
#     else:
#         print("next number")

# while True:
#     n= int(input("0부터 100사이의 수를 입력하세요: "))
#     game(n)

#0~10자연수를 입력받아서 1이면 10까지의 합 2면 20 까지의 합 즉 입력수의 10배까지의 합을 구하는 프로그램

def sum(n):
    res = 0
    for i in range(1, n*10+1):
        res += i
    print(res)
    return res

sum_lambda = lambda n: sum([i for i in range(1, n*10+1)])

while True:
    a= int(input("0~10사이의 자연수를 입력하세요: "))
    sum(a)
    print(sum_lambda(a))
