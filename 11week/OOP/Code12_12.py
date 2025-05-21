import threading
import time

class RacingCar:

    carName = ''
    def __init__(self,name) :
        self.carName = name
    
    def runCar(self) :
        for _ in range(0,3):
            carStr = self.carName +' ~~ 달립니다.\n'
            print(carStr, end= "")
            time.sleep(0.1)

car1 = RacingCar('@자동차1')
car2 = RacingCar('#자동차1')
car3 = RacingCar('$자동차1')

th1 = threading.Thread(target = car1.runCar)
th2 = threading.Thread(target = car1.runCar)
th3 = threading.Thread(target = car1.runCar)

th1.start()
th2.start()
th3.start()