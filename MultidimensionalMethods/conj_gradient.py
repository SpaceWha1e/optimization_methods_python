import math
from typing import Callable
from MultidimensionalMethods import fibonacci
import numpy as np



def partial(function: Callable[[np.ndarray], float], x: np.ndarray, index: int = 0, dx: float = 1e-6) -> float:
    x[index] -= dx
    fl = function(x)
    x[index] += 2 * dx
    fr = function(x)
    x[index] -= dx
    return (fr - fl) / (2 * dx)


def gradient(function: Callable[[np.ndarray], float], x: np.ndarray, eps) -> np.ndarray:
    return np.array(tuple(partial(function, x, index, eps) for index in range(x.size)))


def conj_gradient(function: Callable[[np.ndarray], float], x_start: np.ndarray, eps: float = 1e-6,
                   n_iters: int = 1000) -> np.ndarray:
    assert (x_start.ndim == 1 and "x_start.ndim != 1")
    x_i = x_start.copy()
    x_i_1 = x_start.copy()
    grad_i = - gradient(function, x_i, eps)
    s_i = grad_i.copy()
    x_i_1 = fibonacci(function, x_i, x_i + grad_i, eps)
    cntr = 0
    for cntr in range(n_iters):
        grad_i_1 = gradient(function, x_i, eps)
        s_i_1 = grad_i_1 + s_i * math.pow(np.linalg.norm(grad_i_1), 2)/math.pow(np.linalg.norm(grad_i), 2)
        x_i = x_i_1.copy()
        x_i_1 = fibonacci(function, x_i, x_i - grad, eps)
        if np.linalg.norm(x_i_1 - x_i) < 2 * eps:
            break

    print(f"\tgradient descend::args range : {x_i_1}")
    print(f"\tgradient descend::func probes: {cntr}")

    return (x_i_1 + x_i) * 0.5