# 수(a) 를 입력 받고 짝수인지 홀수인지 판별
# a = int(input("수를 입력하세요: "))

# if a % 2 ==0:
#     print("짝수입니다.")
# else:
#     print("홀수입니다.")

#문제 : 수(a)를 입쳑받고 3의 배수인지 아닌지를 계산
# a = int(input("수를 입력하세요: "))

# if(a %3 ==0):
#     print("3의 배수입니다.")
# else:
#     print("3의 배수가 아닙니다.")

#문제 : 수(a)를 입력받고 짝수이고 3의 배수인지 아닌지를 계산
# a = int(input("수를 입력하세요: "))

# if (a % 2 == 0 and a % 3 == 0):
#     print("짝수이고 3의 배수입니다.")

# elif (a % 2 == 0):
#     print("짝수이고 3의 배수가 아닙니다.")

# elif (a % 3 == 0):
#     print("짝수가 아니고 3의 배수입니다.")

# else:
#     print("짝수도 아니고 3의 배수도 아닙니다.")

# 문제 : 수(a)를 입력받고 5의 배수 또는 7의 배수 인지를 계산
# a= int(input("수를 입력하세요:"))

# if (a % 5 == 0 or a % 7 == 0):
#     print("5의 배수 또는 7의 배수입니다.")
# else:
#     print("5의 배수도 아니고 7의 배수도 아닙니다.")

# 문제 : 수(a)를 입력받고 절대값을 출력하는 함수
# a = int(input("수를 입력하세요: "))
# if a < 0:
#     print(-a)
# else:
#     print(a)

# 문제: 점수를 입력(score)를 받고, 학점을 출력하는 프로그램
#입력성적이 90이상A, 80이상B, 70이상C, 60이상D, 60미만F if~else의 중첩문으로 사용하여라
# score = int(input("성적을 입력하세요: "))
# if score >= 90:
#     print("A")
# else:
#     if score >= 80:
#         print("B")
#     else:
#         if score >= 70:
#             print("C")
#         else:
#             if score >= 60:
#                 print("D")
#             else:
#                 print("F")

score = int(input("성적을 입력하세요: "))
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")
