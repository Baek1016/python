import threading

class SumThread(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self)
        self.n = n

    def run(self):
        total = 0
        for i in range(1, self.n + 1):
            total += i
        print(f"1+2+3+...+ {self.n} = {total}")

# 각각의 합을 계산하는 스레드 생성
th1 = SumThread(1000)
th2 = SumThread(100000)
th3 = SumThread(10000000)

# 스레드 시작
th1.start()
th2.start()
th3.start()

# 모든 스레드가 끝날 때까지 대기
th1.join()
th2.join()
th3.join()