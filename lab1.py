# lab1.py
import matplotlib.pyplot as plt
import random
import argparse


def build_grid(B=100):
    """Равномерная сетка [0, 1/B, ..., (B-1)/B]."""
    return [n / B for n in range(B)]


def generate_uniform_sample(A, rng=None, method="lottery", k=None):
    """
    Алгоритм «равномерного лото»: для каждого случайного x выбираем
    ближайшую ещё не выбранную точку из A и удаляем её.
    Возвращает список выбранных точек в порядке выбора.

    Дополнительно:
      method="lottery"|"random"|"stratified" — способ отбора
      k — сколько точек выбрать (по умолчанию все len(A))
    """
    if rng is None:
        rng = random
    work = list(A)
    n = len(work)
    if k is None:
        k = n

    # Случайная перестановка
    if method == "random":
        idx = list(range(n))
        rng.shuffle(idx)
        return [work[i] for i in idx[:k]]

    # Стратифицированная выборка: по одной точке из каждой страты
    if method == "stratified":
        ordered = sorted(work)
        strata = [[] for _ in range(max(k, 1))]
        for i, v in enumerate(ordered):
            strata[min(i * k // max(n, 1), len(strata) - 1)].append(v)
        result = []
        for s in strata:
            if s:
                result.append(s[rng.randrange(len(s))])
        return result[:k]

    # «Лото» (по умолчанию)
    result = []
    while any(v is not None for v in work) and len(result) < k:
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
        if best_idx is None:
            break
        result.append(work[best_idx])
        work[best_idx] = None
    return result


def plot_histogram(C, bins=20, expected=None, title=None, output=None, show=True):
    plt.figure()
    plt.hist(C, bins=bins, edgecolor="black")
    plt.title(title or "Гистограмма равномерного распределения")
    if expected is not None:
        plt.axhline(expected, color="red", linestyle="--",
                    label="ожидаемое среднее по бинам")
        plt.legend()
    if output:
        plt.savefig(output)
    if show:
        plt.show()
    plt.close()


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("-B", type=int, default=100)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--bins", type=int, default=20)
    p.add_argument("--runs", type=int, default=1, help="число прогонов")
    p.add_argument("--method", choices=["lottery", "random", "stratified"],
                   default="lottery", help="способ отбора точек")
    p.add_argument("--k", type=int, default=None,
                   help="сколько точек выбрать (по умолчанию B)")
    p.add_argument("--chi2", action="store_true",
                   help="вывести статистику хи-квадрат")
    p.add_argument("--output", type=str, default=None,
                   help="сохранить график в файл")
    p.add_argument("--csv", type=str, default=None,
                   help="сохранить счётчики по бинам в CSV")
    p.add_argument("--no-show", action="store_true",
                   help="не открывать окно графика")
    args = p.parse_args(argv)

    rng = random.Random(args.seed)
    A = build_grid(args.B)
    k = args.k if args.k is not None else args.B

    all_samples = []
    all_counts = []
    chi2_per_run = []

    for _ in range(max(args.runs, 1)):
        C = generate_uniform_sample(A, rng=rng, method=args.method, k=k)
        all_samples.append(C)

        counts = [0] * max(args.bins, 1)
        for v in C:
            idx = int(v * args.bins)
            if idx < 0:
                idx = 0
            if idx >= args.bins:
                idx = args.bins - 1
            counts[idx] += 1
        all_counts.append(counts)

        expected = len(C) / args.bins if args.bins > 0 else 0
        if expected > 0:
            chi2_per_run.append(sum((c - expected) ** 2 / expected
                                    for c in counts))
        else:
            chi2_per_run.append(0.0)

    flat = [v for s in all_samples for v in s]
    expected_per_bin = (len(flat) / args.bins) if (args.bins > 0 and flat) else None

    plot_histogram(
        flat,
        bins=args.bins,
        expected=expected_per_bin,
        title=f"Гистограмма ({args.runs} прогон(ов), метод={args.method}, B={args.B})",
        output=args.output,
        show=not args.no_show,
    )

    if args.chi2 and flat:
        total_counts = [0] * args.bins
        for counts in all_counts:
            for i, c in enumerate(counts):
                total_counts[i] += c
        expected = len(flat) / args.bins
        chi2_total = sum((c - expected) ** 2 / expected for c in total_counts)

        df = max(args.bins - 1, 1)
        # грубая верхняя оценка квантиля ~95% без scipy
        critical = df + 2.0 * (2.0 * df) ** 0.5

        avg_chi2 = sum(chi2_per_run) / len(chi2_per_run)
        print(f"Хи-квадрат (объединённый): {chi2_total:.3f}")
        print(f"  df={df}, оценка критич. ~95%: {critical:.2f}")
        print(f"  Средний хи-квадрат по прогонам: {avg_chi2:.3f}")
        if chi2_total < critical:
            print("  Вердикт: нет оснований отвергнуть равномерность")
        else:
            print("  Вердикт: есть отклонение от равномерности")

    if args.csv and all_counts:
        with open(args.csv, "w", encoding="utf-8") as f:
            f.write("run,bin,count\n")
            for r, counts in enumerate(all_counts):
                for b, c in enumerate(counts):
                    f.write(f"{r},{b},{c}\n")
        print(f"CSV сохранён: {args.csv}")


if __name__ == "__main__":
    main()