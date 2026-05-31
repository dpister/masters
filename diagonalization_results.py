from __future__ import annotations
import numpy as np

from math_helper import number


class DiagonalizationResults:
    """"""

    def __init__(
        self,
        x_values: np.ndarray,
        eigenvalues: np.ndarray,
        eigenvectors: np.ndarray,
        cursor: int = 0,
        check_sorted: bool = False,
    ):
        self.x_values = x_values
        self.eigenvalues = eigenvalues
        self.eigenvectors = eigenvectors
        self.cursor = cursor
        if check_sorted and not self.is_sorted():
            self.sort()

    def is_sorted(self) -> np.bool:
        return np.all(self.x_values[:-1] <= self.x_values[1:])

    def sort(self) -> None:
        order = np.argsort(self.x_values)
        self.x_values[:] = self.x_values[order]
        self.eigenvalues[:] = self.eigenvalues[order]
        self.eigenvectors[:] = self.eigenvectors[order]

    @staticmethod
    def new(length: int, number_of_states: int) -> DiagonalizationResults:
        return DiagonalizationResults(
            x_values=np.empty([length]),
            eigenvalues=np.empty([length, number_of_states]),
            eigenvectors=np.empty([length, number_of_states, number_of_states]),
        )

    @staticmethod
    def load_from(path: str) -> DiagonalizationResults:
        loaded_nparrays = np.load(path)
        return DiagonalizationResults(
            x_values=loaded_nparrays["x_values"],
            eigenvalues=loaded_nparrays["eigenvalues"],
            eigenvectors=loaded_nparrays["eigenvectors"],
        )

    def save_to(self, path: str) -> None:
        np.savez(
            path,
            x_values=self.x_values[: self.cursor],
            eigenvalues=self.eigenvalues[: self.cursor],
            eigenvectors=self.eigenvectors[: self.cursor],
        )

    def take_result_from(self, results: DiagonalizationResults) -> None:
        self.x_values[self.cursor] = results.x_values[results.cursor]
        self.eigenvalues[self.cursor] = results.eigenvalues[results.cursor]
        self.eigenvectors[self.cursor] = results.eigenvectors[results.cursor]
        self.cursor += 1
        results.cursor += 1

    def append(self, x_value: number, eigenvalues: np.ndarray, eigenvectors: np.ndarray) -> None:
        self.x_values[self.cursor] = x_value
        self.eigenvalues[self.cursor] = eigenvalues
        self.eigenvectors[self.cursor] = eigenvectors
        self.cursor += 1

    def peek_x_value(self) -> number:
        return self.x_values[self.cursor]

    def has_next(self) -> bool:
        return self.cursor < len(self)

    def __len__(self) -> int:
        return len(self.x_values)

    def reset(self) -> None:
        self.cursor = 0
