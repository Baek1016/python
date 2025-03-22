#문제: 입력점수(score)가 60점이성 "합격", 미만은 "불합격"(기본 if~else문 사용)
# score = int(input("성적을 입력하세요: "))

# if score >= 60:
#     print("합격")
# else:
#     print("불합격")

# #문제: 입력 점수(socre) 80이상 "상", 80미안 60이상 "중", 60미만 "하" (if~else문 사용)
# score = int(input("성적을 입력하세요: "))
# if score >= 80:
#     print("상")
# else:
#     if score >= 60:
#         print("중")
#     else:
#         print("하")

# score = int(input("성적을 입력하세요: "))
# if score >= 80:
#     print("상")
# elif score >= 60:
#     print("중")
# else:
#     print("하")

#문제 월을 입력을 받고 계절을 출력하는 프로그램(3,4,5 봄, 6,7,8 여름, 9,10,11 가을, 12,1,2 겨울)
#1~12월이 아닌 경우 "잘못된 입력" 출력
#month = int(input("월을 입력하세요: "))
# if month == 3 or month == 4 or month == 5:
#     print("봄")
# elif month == 6 or month == 7 or month == 8:
#     print("여름")
# elif month == 9 or month == 10 or month == 11:
#     print("가을")
# elif month == 12 or month == 1 or month == 2:
#     print("겨울")
# else:
#     print("잘못된 입력")

# if 1<=month<=12 :
#     if 3<=month<=5:
#         print("봄")
#     elif 6<=month<=8:
#         print("여름")
#     elif 9<=month<=11:
#         print("가을")
#     else:
#         print("겨울")
# else:
#     print("잘못된 입력")

# 입력 한 두수(a,b)를 받고 거꾸로 뒤집었을때, 큰 수를 출력하는 프로그램 단 a,b는 세자리 수이다.
# a, b = map(int, input("두 개의 세 자리 수를 입력하세요 (공백으로 구분): ").split())

# # 각 자리 수 추출
# a_hundreds = a // 100
# a_tens = (a // 10) % 10
# a_units = a % 10

# b_hundreds = b // 100
# b_tens = (b // 10) % 10
# b_units = b % 10

# # 뒤집은 숫자 계산
# a_reversed = a_units * 100 + a_tens * 10 + a_hundreds
# b_reversed = b_units * 100 + b_tens * 10 + b_hundreds

# # 뒤집은 숫자 출력 및 비교
# print(f"뒤집은 첫 번째 수: {a_reversed} \t 두 번째 수: {b_reversed}")


# if a_reversed > b_reversed:
#     print(f"뒤집은 숫자 {a_reversed}인 a가 더 큽니다.")
# else:
#     print(f"뒤집은 숫자 {b_reversed}인 b가 더 큽니다.")

# 입력 한 두수(a,b)를 받고 거꾸로 뒤집었을때, 큰 수를 출력하는 프로그램(단 a,b는 자리수의 제한이 없으며 해결방식은 문자열로 인식해서 해결한다.)
# a, b ,c = map(int, input("두 개의 입력하세요 (공백으로 구분): ").split())

# a_reversed = int(str(a)[::-1])
# b_reversed = int(str(b)[::-1])
# c_reversed = int(str(c)[::-1])

# print(f"뒤집은 첫 번째 수: {a_reversed} \t 두 번째 수: {b_reversed}")

# if a_reversed > b_reversed:
#     print(f"뒤집은 숫자 {a_reversed}인 a가 더 큽니다.")
# elif a_reversed < b_reversed:
#     print(f"뒤집은 숫자 {b_reversed}인 b가더 큽니다.")
# else:
#     print("두 수가 같습니다.")