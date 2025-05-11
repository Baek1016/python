import math
# 완전수란 약수 중 자기 자신을 제외하고 더했을 때 자기 자신이 나오는 수
def completenum(n):
    result = []  # 완전수를 저장할 리스트
    for num in range(1, n + 1):  # 1부터 n까지 반복
        hap = 0
        for i in range(1, num):  # 자기 자신을 제외한 약수의 합 계산
            if num % i == 0:
                hap += i
        if hap == num:  # 약수의 합이 자기 자신과 같으면 완전수
            result.append(num)
    return result

def justcn(n):
    hap = 0
    for i in range(1, n + 1):
        if n % i == 0:
            hap += i
    if (hap -n) == n:
        print(f"{n}은 완전수입니다.")
    else:
        print(f"{n}은 완전수가 아닙니다.")
    
def licn(n):
    hap = 0
    a = []
    for i in range(1, n + 1):
        if n % i == 0:
          a.append(i)
    if sum(a) == n:
        print(f"{n}은 완전수입니다.")
    else:
        print(f"{n}은 완전수가 아닙니다.")

N = int(input("수 입력: "))

perfect_numbers = completenum(N)
justcn(N)
licn(N)

if perfect_numbers:
    print(f"{N}까지의 완전수: {perfect_numbers}")
else:
    print(f"{N}까지 완전수가 없습니다.")

