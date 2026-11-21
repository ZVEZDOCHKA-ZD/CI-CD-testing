import random
import pytest
import lab1


# ---------- Unit-тесты на build_grid ----------

def test_build_grid_length():
    A = lab1.build_grid(100)
    assert len(A) == 100


def test_build_grid_values():
    A = lab1.build_grid(100)
    assert A[0] == 0.0
    assert A[-1] == 0.99
    assert all(0.0 <= v < 1.0 for v in A)


def test_build_grid_custom_size():
    A = lab1.build_grid(10)
    assert A == [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]


# ---------- Unit-тесты на generate_uniform_sample ----------

def test_sample_length_equals_input():
    A = lab1.build_grid(20)
    C = lab1.generate_uniform_sample(A, rng=random.Random(0))
    assert len(C) == len(A)


def test_sample_is_permutation_of_input():
    A = lab1.build_grid(50)
    C = lab1.generate_uniform_sample(A, rng=random.Random(0))
    assert sorted(C) == sorted(A)


def test_sample_does_not_mutate_input():
    A = lab1.build_grid(10)
    original = list(A)
    lab1.generate_uniform_sample(A, rng=random.Random(0))
    assert A == original


def test_sample_deterministic_with_same_seed():
    A = lab1.build_grid(30)
    C1 = lab1.generate_uniform_sample(A, rng=random.Random(42))
    C2 = lab1.generate_uniform_sample(A, rng=random.Random(42))
    assert C1 == C2


def test_sample_empty_input():
    assert lab1.generate_uniform_sample([], rng=random.Random(0)) == []


# ---------- Интеграционный / smoke-тест на main ----------

def test_main_runs_and_calls_show(monkeypatch):
    """Прогоняем весь пайплайн с подменённым plt.show (без открытия окна)."""
    called = {}

    def fake_show():
        called["show"] = True

    monkeypatch.setattr("matplotlib.pyplot.show", fake_show)
    lab1.main([])
    assert called.get("show") is True