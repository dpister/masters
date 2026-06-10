from dataclasses import dataclass

import numpy as np

from product_states import ProductStateMatrix
from spin_ring import SpinRing
from math_helper import number


@dataclass
class Results:
    """"""

    product_state_matrix: ProductStateMatrix
    x_values: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    spin_rings: list[SpinRing]
    temperatures: list[number]

    spin_expectation_values: np.ndarray | None = None
    toroidal_moments: np.ndarray | None = None
    spin_correlation_values: np.ndarray | None = None
    magnetizations: np.ndarray | None = None
    alignments: np.ndarray | None = None

    spin_expectation_values_thermal: np.ndarray | None = None
    toroidal_moments_thermal: np.ndarray | None = None
    spin_correlation_values_thermal: np.ndarray | None = None
    magnetizations_thermal: np.ndarray | None = None
    alignments_thermal: np.ndarray | None = None

    def sort(self) -> None:
        order = np.argsort(self.x_values)
        self.x_values.sort()
        self.eigenvalues[:] = self.eigenvalues[order]
        self.eigenvectors[:] = self.eigenvectors[order]
        self.spin_rings[:] = [self.spin_rings[i] for i in order]
        if self.spin_correlation_values is not None:
            self.spin_correlation_values[:] = self.spin_correlation_values[order]
        if self.spin_expectation_values is not None:
            self.spin_expectation_values[:] = self.spin_expectation_values[order]
        if self.toroidal_moments is not None:
            self.toroidal_moments[:] = self.toroidal_moments[order]
        if self.alignments is not None:
            self.alignments[:] = self.alignments[order]
        if self.magnetizations is not None:
            self.magnetizations[:] = self.magnetizations[order]
