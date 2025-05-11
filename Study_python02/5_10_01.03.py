#n에다가 자연수(정수)를 입력받고, N의 약수를 출력하는 프로그램
#약수 :n을 1~n까지 나눳을떄 나눠 떨어지면 약수
def divisor(n):
    for i in range(1, n + 1):
        if n % i == 0:
            print(i, end=" ")
    print()  # 줄바꿈을 위해 추가

n = int(input("자연수 n을 입력하세요: "))
res = divisor(n)
print(f"{n}의 약수는 {res}", end="")


# def divisor(n):
#     # 약수를 구하는 함수
#     result = []
#     for i in range(1, n + 1):
#         if n % i == 0:
#             result.append(i)
#     return result

# def common_divisors(a, b):
#     # 두 수의 공약수를 구하는 함수
#     common = []
#     for i in range(1, min(a, b) + 1):  # 두 수 중 작은 값까지만 확인
#         if a % i == 0 and b % i == 0:  # 공약수 조건
#             common.append(i)
#     return common

# def gcd(a, b):
#     # 최대 공약수를 구하는 함수
#     max_divisor = 1
#     for i in range(1, min(a, b) + 1):  # 두 수 중 작은 값까지만 확인
#         if a % i == 0 and b % i == 0:  # 공약수 조건
#             max_divisor = i  # 가장 큰 공약수를 저장
#     return max_divisor

# # 사용자 입력
# n1 = int(input("첫 번째 자연수를 입력하세요: "))
# n2 = int(input("두 번째 자연수를 입력하세요: "))

# # 약수 출력
# print(f"{n1}의 약수: {divisor(n1)}")
# print(f"{n2}의 약수: {divisor(n2)}")

# # 공약수 출력
# common = common_divisors(n1, n2)
# print(f"{n1}과 {n2}의 공약수: {common}")

# # 최대 공약수 출력
# print(f"{n1}과 {n2}의 최대 공약수: {gcd(n1, n2)}")