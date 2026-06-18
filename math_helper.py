import numpy as np
import math

type number = int | float
type complex_number = int | float | complex


PI = math.pi
BOHR_MAGNETON = MU_B = 0.6717
LANDE_FACTOR = 2


e_x = unit_vector_x_direction = np.array([1, 0, 0])
e_y = unit_vector_y_direction = np.array([0, 1, 0])
e_z = unit_vector_z_direction = np.array([0, 0, 1])


indices_mapping = {"x": 0, "y": 1, "z": 2}


def get_rotation_matrix_around_x_axis(angle: number) -> np.ndarray:
    return np.array(
        [
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)],
        ]
    )


def get_rotation_matrix_around_y_axis(angle: number) -> np.ndarray:
    return np.array(
        [
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)],
        ]
    )


def get_rotation_matrix_around_z_axis(angle: number) -> np.ndarray:
    return np.array(
        [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1],
        ]
    )


def get_x_unit_vector_tilted_in_xy_plane(angle: number) -> np.ndarray:
    return np.array([math.cos(angle), 0, math.sin(angle)])


def degree_to_radians(x_value: number) -> number:
    return x_value / 360 * 2 * PI


def is_almost_real(array: np.ndarray, atol: number = 1e-12) -> bool:
    return np.allclose(np.imag(array), 0, atol=atol, rtol=0)


def sort_eigenvalues_and_eigenvectors(eigenvalues: np.ndarray, eigenvectors: np.ndarray) -> None:
    order = np.argsort(eigenvalues)
    eigenvalues[:] = eigenvalues[order]
    eigenvectors[:, :] = eigenvectors[:, order]


def flatten(x_values: np.ndarray, y_values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    num_x_values, num_y_values_per_x_value = y_values.shape
    new_x_values = np.empty(num_x_values * num_y_values_per_x_value, dtype=x_values.dtype)
    new_y_values = np.empty(num_x_values * num_y_values_per_x_value, dtype=y_values.dtype)

    for i, x_value in enumerate(x_values):
        for j, y_value in enumerate(y_values[i]):
            new_x_values[i * num_y_values_per_x_value + j] = x_value
            new_y_values[i * num_y_values_per_x_value + j] = y_value

    return new_x_values, new_y_values
