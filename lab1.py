# lab1.py
import matplotlib.pyplot as plt
import random


def build_grid(B=100):
    """Равномерная сетка [0, 1/B, ..., (B-1)/B]."""
    return [n / B for n in range(B)]


def generate_uniform_sample(A, rng=None):
    """
    Алгоритм «равномерного лото»: для каждого случайного x выбираем
    ближайшую ещё не выбранную точку из A и удаляем её.
    Возвращает список выбранных точек в порядке выбора.
    """
    if rng is None:
        rng = random
    work = list(A)          # не мутируем входной список
    result = []
    while any(v is not None for v in work):
        x = rng.random()
        best_idx = None
        best_dist = None
        for i, v in enumerate(work):
            if v is None:
                continue
            d = abs(x - v)
            if best_dist is None or d <= best_dist:
                best_dist = d
                best_idx = i
        result.append(work[best_idx])
        work[best_idx] = None
    return result


def plot_histogram(C, bins=20):
    plt.hist(C, bins=bins, edgecolor="black")
    plt.title("Гистограмма равномерного распределения")


def main():
    A = build_grid(100)
    C = generate_uniform_sample(A)
    plot_histogram(C)
    plt.show()


if __name__ == "__main__":
    main()
