def cm(coffee):
    print("#1.뜨거운 물을 준비한다.")
    print("#2.종이컵을 준비한다.")

    if coffee == 1:
        print("#3.보통 커피를 탄다.")
    elif coffee ==2:
        print("#3.설탕커피를 탄다.")
    elif coffee ==3:
        print("블랙커피를 탄다.")
    else:
        print("아무거나 찬다.\n")

    print("#4.물 붓는다.\n")
    print("#5.스푼으로 젓는다.\n")
    print("#6.완성입니다.\n")

coffee =0
while (1) :

    coffee = int(input("어떤 커피 드릴까요?(1:보통, 2:설탕. 3:블랙)"))

    print(cm(coffee))