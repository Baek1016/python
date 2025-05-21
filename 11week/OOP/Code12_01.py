class Car :
    #filed(속성=변수)
    color = ""
    speed = 0

    #method(기능-클래스내 함수 )
    def upSpeed(self,value) :
        self.speed += value

    def downSpeed(self, value) :
        self.speed -=value