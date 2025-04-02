#1.입력한 수식 계산 2. 두수사이의 합계:

n1 = int(input("1.입력한 수식 계산 2. 두수사이의 합계:"))

if n1 == 1:
    s1= input("***수식을 입력하세요***")
    
    print(eval(s1))
else:
    n2 = int(input("***첫번째 수를 입력하세요"))
    n3 = int(input("***두번째 수를 입력하세요"))
    sum = 0

    for i in range(n2,n3+1,1):
        sum += i

    print(sum)