###중첩 for문문

# for i in range(0,3,1):
#     for k in range(0,2,1):
#         print("파이썬(i값: %d k값 : %d)" % (i,k))

#중첩 for문 활용 2단 부터 9단까지 구구단 세로로 출력
# for i in range(2,10,1):
#     for k in range(1,10,1):
#         print("%d x %d = %d" % (i,k,i*k))
#     print("\n")

# for i in range(1,10,1):
#     for k in range(2,10,1):
#         print("%d x %d = %d" % (k,i,i*k),end="  ")
#     print("\n")

#수를 입력(N)받고 N 이하의 각각의 숫자에 대해서 짝수의 개수(su) 구하기 (중첩 for문으로)
N = int(input("수를 입력하세요: "))

for i in range(1,N+1,1):
    su = 0
    for k in range(1,i+1,1):
        if k % 2 == 0:
            su += 1
print("%d의 짝수의 개수: %d" % (i,su))
print("\n")