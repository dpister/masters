from abc import ABC, abstractmethod

import numpy as np

from results import Results


class Plotter(ABC):
    """"""

    @abstractmethod
    def add_points(
        self,
        results: Results,
        color_map: np.ndarray,
    ) -> None: ...

    @abstractmethod
    def save(self, folder: str) -> None: ...
