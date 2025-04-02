# #####튜플
# # 리스트는[] dic은{} 튜플은()으로 표현한다.
# # 튜플은 리스트와 비슷하지만 수정이 불가능하다.
# tt1=(10,20,30)
# print(tt1)
# tt2 =10,20,30
# print(tt2)
# # 튜플이라도 단일은 tuple인식이 안되지만 ,을 넣으면 tuple로 인식이 된다.
# tt3=(10)
# print(tt3)
# tt4=(10,)
# print(tt4)
# tt5=10
# print(tt5)
# tt6=10,
# print(tt6)
# # 튜플은 수정이 불가능하다.
# # 튜플 전체 삭제는 가능하다.

# tt1=[10,20,30]
# # tt1.append(40)
# tt1[0]=100
# del tt1[0]
# print(tt1)


# aa = [10,20,30,40]
# print(aa[0],aa[3]) #앞에서 부터 [0]
# print(aa[-1],aa[-4]) #뒤에서 부터 [-1]
# print(aa[0:3]) # [0:3]은 0~2까지
# print(aa[2:4]) # [2:4]는 2~3까지
# print(aa[:2]) # [:2]는 0~1까지
# print(aa[2:]) # [2:]는 2~끝까지

aaa=[10,20,30,40,50,60,70]
print(aaa[::2])
print(aaa[::3])
print(aaa[::-1])
print(aaa[::-2])
aaa[1] =200
print(aaa)
aaa[2:4] = [300,400]
print(aaa)
del aaa[1]
print(aaa)
