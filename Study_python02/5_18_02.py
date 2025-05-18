# #추상 메서드(추상 메서드 사용시 반드시 메서드 오버라이딩을 해야함.)
# class SuperClass:
#     #추상 메서드
#     def method(self):
#         pass

# class SubClass1(SuperClass):
#     # 메서드 오버라이딩
#     def method(self):
#         print("SubClass method")

# class SubClass2(SuperClass):
    
#     pass

# sub1= SubClass1()
# sub2= SubClass2()

# sub1.method()
# sub2.method() # 에러 발생

#자동차 세대가 경주하는 코드
import time
import threading

class RacingCar:
    carName= ""
    def __init__(self,name):
        self.carName= name
    
    def runCar(self):
        for _ in range(0,3):
            carStr = self.carName + "~달립니다.\n"
            print(carStr,end = "")
            time.sleep(1)

car1 =RacingCar("소나타")
car2 =RacingCar("그랜저")
car3 =RacingCar("아반떼")

th1 = threading.Thread(target=car1.runCar)
th2 = threading.Thread(target=car2.runCar)
th3 = threading.Thread(target=car3.runCar)

th1.start()
th2.start()
th3.start()