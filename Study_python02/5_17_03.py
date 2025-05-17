class Car:
    #filed 속성(변수)
    #인스턴스 변수:각 객체만의 고유한 값
    color = ""
    speed = 0
    #클래스 변수 :모든 객체가 함께 쓰는 값(공유)
    count = 0

    #method 기능(함수)

    #기본 생성자
    def __init__(self):
        self.speed = 0
        Car.count += 1

myCar1,myCar2 = None, None

#인스턴스 생성
myCar1 = Car()
myCar1.speed = 30

myCar2 = Car()
myCar2.speed = 50

print("자동차1의 현재속도는 %dkm, 생상된 자동차는 총 %d입니다." % (myCar1.speed, myCar1.count))
print("자동차2의 현재속도는 %dkm, 생상된 자동차는 총 %d입니다." % (myCar2.speed, Car.count))
