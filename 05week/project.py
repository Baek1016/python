#2중 for문을 이용하여 2단부터 9단까지 구하기

for k in range(2,10):
    print("#  %d단  #" % k, end = " ")
print("\n")

for i in range(1,10):
    for j in range(2,10):
        print("%dX %d = %2d" % (j,i,j*i), end = " ")
    print("\n")
    