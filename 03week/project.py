a = int(input("입력 진수 결정(16/10/8/2)"))
b = input("값 입력")

c= int(b, a)

print(f"16진수 ==> {hex(c)}")
print(f"10진수 ==> {c}")
print(f" 8진수 ==> {oct(c)}")
print(f" 2진수 ==> {bin(c)}")
