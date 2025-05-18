# class Car:
#     speed = 0

#     def upSpeed(self,value):
#         self.speed += value
#         print("현재 속도(슈퍼 클래스): %d" %self.speed)

# #method overriding 상위 클래스의 메소드를 하위 클래스에서 재정의
# class Sedan(Car):

#     def upSpeed(self,value):
#         self.speed += value

#         if self.speed>150:
#             self.speed = 150
#         print("현재 속도(서브 클래스): %d" %self.speed)

# # Truck 클래스는 Car 클래스를 상속받음
# class Truck(Car):
#     #pass는 부모 클래스의 속성을 그대로 사용하겠다는 의미
#     pass

# sedan1, truck1 = None,None

# sedan1= Sedan()
# truck1 = Truck()

# print("승용차-->",end=" ")
# sedan1.upSpeed(200)

# print("트럭-->",end=" ")
# truck1.upSpeed(200)

class Line:
    length = 0
    def __init__(self,length):
        self.length = length
        print(self.length,"길이의 선이 생성되었습니다.")

    def __del__(self): # 소멸자
        print(self.length,"길이의 선이 제거되었습니다.")

    def __repr__(self):# 인스턴스를 print()문으로 출력할 때 실행
        return "선의 길이: "+str(self.length)

    def __add__(self,other):# 인스턴스끼리 더하기시에 실행
        return self.length +other.length
    
    def __lt__(self,other):# lt는 비교 연산자(less than)
        return self.length < other.length
    
    def __eq__(self,other):# eq는 비교 연산자(equal)
        return self.length == other.length
    
myLine1 =Line(100)
myLine2 =Line(200)

print(myLine1)

print("두 선의 길이 합: ",myLine1 + myLine2)

if myLine1 < myLine2:
    print("myLine2이 더 길다.")
elif myLine1 == myLine2:
    print("같다.")
else:
    print("모른다.")

del(myLine1)