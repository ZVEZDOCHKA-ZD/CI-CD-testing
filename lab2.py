import numpy as np

def poly_value(x, coeffs): # Вычисляет значение полинома в точке x
    result = coeffs[0]
    for coeff in coeffs[1:]:
        result = result * x + coeff
    return result

def proizv(x, coeffs): # Вычисляет значение производной полинома в точке
    n = len(coeffs) - 1
    result = coeffs[0] * n
    for i, coeff in enumerate(coeffs[1:-1], 1):
        result = result * x + coeff * (n - i)
    return result

def newton_method(x0, coeffs, tol=1e-20, max_iter=100): #Метод Ньютона для поиска одного корня
    x = complex(x0)
    for i in range(max_iter):
        fx = poly_value(x, coeffs)
        fpx = proizv(x, coeffs)
        
        # Проверка на нулевую производную
        if abs(fpx) < 1e-15:
            x += complex(0.1, 0.1)
            continue
        x1 = x - fx / fpx # Итерация Ньютона
        if abs(x1 - x) < tol: # Проверка точности
            return x1, i + 1, True
        x = x1

    return x, max_iter, False

def deflate_polynomial(coeffs, root):
    """
    Дефляция полинома: деление на (x - root) по схеме Горнера.
    Возвращает коэффициенты полинома степени на 1 меньше.
    """
    n = len(coeffs)
    new_coeffs = np.zeros(n - 1, dtype=complex)
    
    new_coeffs[0] = coeffs[0]
    for i in range(1, n - 1):
        new_coeffs[i] = new_coeffs[i - 1] * root + coeffs[i]
    
    return new_coeffs

def newton_deflation(coeffs, tol=1e-10, max_iter=100, initial_guesses=[1, 1-1j, -1-1j, -1]): # [1, 1-1j, -1-1j, -1] ||  [(0.9+0.3j), (-0.3+0.9j), (-0.9-0.3j), (0.3-0.9j)]
    """
    coeffs - коэффициенты полинома от старшей к младшей
    tol - точность
    max_iter - максимальное число итераций
    initial_guesses - начальные приближения (опционально)
    """
    coeffs = np.array(coeffs, dtype=complex)
    current_coeffs = coeffs.copy()
    degree = len(current_coeffs) - 1
    
    A = []
    
    # Поиск всех корней
    for i in range(degree):
        # Выбор начального приближения
        if i < len(initial_guesses):
            x0 = initial_guesses[i]
        
        # Поиск корня методом Ньютона
        root, iter_count, converged = newton_method(x0, current_coeffs, tol, max_iter)
        A.append(root)
        
        # Дефляция полинома (кроме последнего корня)
        if i < degree - 1:
            current_coeffs = deflate_polynomial(current_coeffs, root)
    return A


print("\n" * 6)  
print("\nВведите коэффициенты полинома.")
coeff_input = input("Коэффициенты: ").strip() # Ввод полинома
coeffs = list(map(float, coeff_input.split()))
                
A = newton_deflation(coeffs, tol=1e-12) # Решение полинома
    
# Вывод результатов
print("\nНайденные корни:")
for i, (root_str) in enumerate(zip(A), 1):
    print(f"x{i} = {root_str}")
