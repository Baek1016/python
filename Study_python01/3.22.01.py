# print("안녕하세요")
# print("안녕하세요")
# print("안녕하세요")
# print("안녕하세요")
# print("안녕하세요")

# for i in range(0,5,1):
#     print("%d : 안녕하세요" % i)
# print("안녕하세요")

# for i in range(1,6,1):
#     print("%d : 안녕하세요" % i)
# print("안녕하세요")

# for i in range(5,0,-1):
#     print("%d : 안녕하세요" % i)
# print("안녕하세요")

# for i in range(1,6,1):
#     print("%d : 안녕하세요" % i,end='    ')
# print("안녕하세요")

#1~10까지 합(hap)을 구하는 프로그램
#hap = 1+2+3+4+5+6+7+8+9+10
# hap =0
# for i in range(1,11,1):
#     hap += i
#     print("%2d : 1~%2d까지의 (hap): %3d" % (i,i,hap))

#0과 1000사이의 합계
# hap = 0
# for i in range(0,1000,1):
#     hap += i
# print("0~1000까지의 합: ",hap)

#500부터 1000까지의 홀수의 합
# hap = 0
# for i in range(501,1000,2):
#     hap += i
# print("500~1000까지의 홀수의 합: ",hap)

#키보드로 입력한 수(num)까지의 합계
# num = int(input("수를 입력하세요: "))
# hap = 0
# for i in range(1,num+1,1):
#     hap += i
# print("1~%d까지의 합: %d" % (num,hap))

#시작값,끝값,증가값까지 사용자 입력한후 합계
# n1= int(input("시작값을 입력하세요: "))
# n2= int(input("끝값을 입력하세요: "))
# n3= int(input("증가값을 입력하세요: "))
# hap = 0
# for i in range(n1,n2+1,n3):
#     hap += i
# print("%d~%d까지의 %d씩 증가한 값의 합: %d" % (n1,n2,n3,hap))

# 문제: 월 화 수 목 금 토 일을 차례로 세로와 가로로 출력
# for i in ['월','화','수','목','금','토','일']:
#     print("%s" % i)
# for i in ['월','화','수','목','금','토','일']:
#     print("%s" % i,end='')


#사용자가 입력(dan)한 숫자의 단에서 구구단을 출력(아래 결과와 같이 출력)
# dan = int(input("단을 입력하세요."))
# for i in range(1,10,1):
#     print("%2d X %2d = %2d" % (dan, i, dan * i))
# print("...")

#수를 입력받고 (N)짝수, 홀수를 판별하는 프로그램
# for i in range(1,5,1):
#     num = int(input("수를 입력하세요: "))

#     if num % 2 ==0:
#         print("짝수입니다.")
#     else:
#         print("홀수입니다.")

# 4개의 수를 입력받고(N) 짝수, 홀수를 판별하는 프로그램을 리스트 변수(li)를 사용해라(append를 사용하여 li안에 추가하여라라)
# li = []
# for i in range(0,4,1):
#     N = int(input("수를 입력하세요: "))
#     li.append(N)

# for i in li:
#     if i % 2 ==0:
#         print("%d는 짝수입니다." % i)
#     else:
#         print("%d는 홀수입니다." % i)

#5개의 점수를 입력(N) 받고 평균(평균)보다 낮은 수들을 구하는 프로그램(sum(),len()를 이용)
# li = []
# for i in range(0,5,1):
#     N = int(input("수를 입력하세요: "))
#     li.append(N)

# hap = sum(li)
# avg = hap / len(li)
# print("평균: ",avg)
# for i in li:
#     if i < avg:
#         print("%d는 평균보다 낮습니다." % i)
