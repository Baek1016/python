def calac(v1,v2,op):
    result = 0
    if op == '+':
        result = v1 + v2
    elif op == '-':
        result = v1 - v2
    elif op == '*':
        result = v1 * v2
    elif op == '/':
        result = v1 / v2
    elif op == '%':
        result = v1 % v2
    return result

res =0 
var1,var2,oper =0,0,""
oper = input("계산할 연산자를 입력하세요: (+,-,*,/,%): ")
var1 = int(input("계산할 숫자를 입력하세요.:"))
var2 = int(input("계산할 숫자를 입력하세요.:"))

res = calac(var1,var2,oper)

print(f"{var1} {oper} {var2} = {res}")