#함수 코드 부분
def plus(v1,v2): # 함수 실행
    result = 0
    result = v1 + v2
    return result # 함수 호출한 한곳으로 반환 및 종료

a = int(input("첫번째 숫자 입력: "))
b = int(input("두번째 숫자 입력: "))

hap = 0
hap = plus(a,b)

print("100과 200plus()함수 결과는 %d입니다." % hap)
print(f"100과 200plus()함수 결과는 {hap}입니다.")