import matplotlib.pyplot as plt
import random

# равномерное лото
B = 100
A = [n / 100 for n in range(B)]
print(A)

C = []
n = len(A)
while n > 0:
    x = random.random()
    y = 1
    i = 0
    i1 = 0
    B = len(A)
    while i < B:
        if A[i] is not None and y >= abs(x - A[i]):
            y = abs(x - A[i])
            i1 = i
        i += 1
    C.append(A[i1])
    A[i1] = None
    n -= 1

# plot(C)
# title("Равномерно распределенный ПСЕВДОслuчайный процесс")
# M = mean(C)
# D = var(C)

plt.hist(C, bins=20, edgecolor='black')
plt.title('Гистограма равномерного распределения')
plt.show()
