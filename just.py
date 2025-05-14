# " "빈칸과 *를 찍고 for문이용해서 피라미드 모양으로 출력하기

for i in range(1, 6):
    for j in range(1, 6 - i):
        print(" ", end="")
    for k in range(1, i * 2):
        print("*", end="")
    print()

# for문을 이용해서 아무 거나 말들기
