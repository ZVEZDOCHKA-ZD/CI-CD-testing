import matplotlib.pyplot as plt
import random

n = 0
A = []
C = 0
# равномерное лото
B = 100;
while n<B:
    A.append(n/100)
    n = n + 1;
print(A)

while n>0:
    x = random()
    y = 1
    i = 1
    i1 = 1
    B = len(A)
    while i<B:
        if y >= abs(x - A(i)):
            y = abs(x - A(i))
            i1 = i
        i = i+1
    C[n] = A[i1]
    A[i1] = []
    n = n - 1
#plot(C)
#title("Равномерно распределенный ПСЕВДОслучайный процесс")
#M = mean(C)
#D = var(C)

plt.hist(C, bins=20, edgecolor='black')
plt.title('Гистограма равномерного распределения')
plt.show()