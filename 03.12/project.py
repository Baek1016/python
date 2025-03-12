# inch 단위를 cm 단위로 변환하는 프로그램 (inchTocm.py)

inch = float(input("inch 단위를 입력하세요: "))
cm = inch * 2.54

print(f"{inch} inch는 {cm} cm입니다.")


# 킬로그램 단위를 파운드 단위로 변환하는 프로그램 (kgToPound.py)

kg = float(input("킬로그램 단위를 입력하세요: "))
pound = kg * 2.20462

print(f"{kg} kg은 {pound} pound입니다.")




# 원의 반지름을 입력받아 둘레와 넓이를 계산하는 프로그램 (CircleCal.py)

import math

radius = float(input("원의 반지름을 입력하세요: "))

circumference = 2 * math.pi * radius
area = math.pi * radius ** 2

print(f"원의 둘레는 {circumference}입니다.")
print(f"원의 넓이는 {area}입니다.")