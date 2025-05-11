# def func1():
#     global a # 전역변수 a를 사용하겠다고 선언
#     a =10 # 지역변수 >> 전역변수
#     print("func1()에서 a의 값 %d" % a)

# def func2():
#     print("func2()에서 a의 값 %d" % a)

# a = 20 # 전역변수

# func1()
# func2()

# def func1():
#     result = 100
#     return result

# def func2():
#     print("반환값이 없는 함수 실행")

# hap = 0

# hap = func1() # func1()의 반환값을 hap에 저장
# print("func1()의 반환값 : %d" % hap)
# func2() # 반환값이 없는 함수 실행

# def func1(x):
#     x+=1
#     print("1증가 했습니다.")
#     return x

# def func2(x):
#     x+=1
#     print("1증가 했습니다.")

# a= 10 

# a= func1(a)
# print("func1()의 반환값 : %d" % a)

# func2(a)
# print("func2()의 반환값 : %d" % a)


def multi(v1,v2):
    retList = []
    res1 = v1 +v2
    res2 = v1 -v2
    retList.append(res1)
    retList.append(res2)
    return retList

myList= []
hap, sub=(0,0)
myList = multi(10,20)
hap = myList[0]
sub = myList[1]

print("multi()돌려준값 ==> %d,%d" % (hap, sub))