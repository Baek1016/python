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
