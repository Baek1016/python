# def para_func(v1,v2,v3 = 0):
#     result = 0
#     result = v1 + v2 + v3
#     return result


# 함수 정의에서 *를 사용하면, 함수가 임의 개수의 인자를 받을 수 있습니다. 이 인자들은 튜플(tuple)로 함수  내부에전달됩니다.
def para_func (*para):
    result = 0
    for i in para:
        result += i
    return result

hap = 0

hap = para_func(10,20)
print("매개 변수가 2개인 경우 :%d ", hap)
hap = para_func(10,20,30)
print("매개 변수가 3개인 경우 :%d ", hap)

def dic_func(**para):
    for k in para.keys():
        print("%s --> %d명입니다." % (k,para[k]))

dic_func(트와이스 =9, 소녀시대 = 8, 걸스데이는 = 4, 블랙핑크 = 4)

