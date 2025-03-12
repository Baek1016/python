# circle Radius to calculate circumference and area of a circles
import math

radius = float(input("원의 반지름을 입력하세요: "))

circumference01 = 2 * math.pi * radius
circumference02 = 2 * 3.14 * radius

area01 = math.pi * radius ** 2
area02 = 3.14 * radius ** 2

print(f"원의 둘레는 {circumference01}입니다.")
print(f"원의 둘레는", circumference02 , "입니다.")

print(f"원의 넓이는 {area01}입니다.")
print(f"원의 넓이는" , area02 , "입니다.")