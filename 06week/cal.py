#함수 선언
def calc(v1,v2,op):
    result = 0 #리턴해야할 값값
    
    if op == "+":
        result = v1 + v2
    elif op == "-":
        result = v1 - v2
    elif op == "*":
        result = v1 * v2
    elif op == "/":
        if v2 == 0:
            print("0으로 나눌 수 없습니다.")
            return 0
        else:
            result = v1 / v2

    return result
#전역 변수
res = 0

var1,var2,oper=0,0,""

#메인 코드
oper = input("계산을 입력하세요(+,-,*,/)")
var1 = int(input("첫번째 숫자:"))
var2 = int(input("두번째 숫자:"))

res = calc(var1,var2,oper)

print("%d %s %d = %d" % (var1,oper,var2,res))