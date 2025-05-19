# print("평균 학점을 계산 해드립니다.")
# math=int(input("수학 점수입력:"))
# ko=  int(input("국어 점수입력:"))
# eng= int(input("영어 점수입력:"))
# sci= int(input("과학 점수입력:"))

# sum=(math+ko+eng+sci)
# avg=sum/4.0

# print(f"평균 학점은 {avg}입니다.", end = "")
import math

res = list(map(int,input("점수를 입력하시오").split()))

avg = sum(res) /len(res)

print(f"평균 점수는 {avg} 입니다.")