import math
from math_helper import number
import numpy as np


def calculate_canonical_partition_sum(temperature: number, eigenvalues: np.ndarray) -> number:
    z = 0
    for eigenvalue in eigenvalues:
        z += math.exp(-1 / temperature * eigenvalue)
    return z


def calculate_thermal_expectation_value(
    temperature: number,
    expectation_values: np.ndarray,
    eigenvalues: np.ndarray,
) -> complex:
    canonical_sum = calculate_canonical_partition_sum(temperature=temperature, eigenvalues=eigenvalues)
    result = 0
    for expectation_value, eigenvalue in zip(expectation_values, eigenvalues):
        result += math.exp(-eigenvalue / temperature) * expectation_value
    return result / canonical_sum
