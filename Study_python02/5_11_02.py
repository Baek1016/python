# def func1():
#     global a # 전역변수 a를 사용하겠다고 선언
#     a =10 # 지역변수 >> 전역변수
#     print("func1()에서 a의 값 %d" % a)

# def func2():
#     print("func2()에서 a의 값 %d" % a)

# a = 20 # 전역변수

# func1()
# func2()

def func1():
    result = 100
    return result

def func2():
    print("반환값이 없는 함수 실행")

hap = 0

hap = func1() # func1()의 반환값을 hap에 저장
print("func1()의 반환값 : %d" % hap)
func2() # 반환값이 없는 함수 실행
