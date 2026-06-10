from __future__ import annotations

from typing import Any

import numpy as np
from math_helper import number


class SpinState:
    """
    Helper class to simplify implementation of Kronecker delta,
    which lets you compare two different product states.
    For example, suppose you have a product state (m0, m1, m2, ..., mN-1)
    with m_i in {-s_i, -s_i+1, ... s_i-1, s_i} and another product state (m0', m1', m2', ..., mN-1').
    Now suppose you want to check whether two states are equal, except m1 = m1'-1.
    You can compare the two states using the "changed" method.
    equal = state1 == state2.changed(1, -1)
    """

    def __init__(self, array: np.ndarray):
        self.nparray = np.copy(array)

    def changed(self, ind: int, shift: int) -> SpinState:
        """
        Returns a copy of the state with the entry at the index shifted.
        """
        copy = np.copy(self.nparray)
        copy[ind] += shift
        return SpinState(copy)

    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, SpinState):
            return False
        return np.array_equal(self.nparray, obj.nparray)

    def __getitem__(self, index: int) -> number:
        return self.nparray[index]


class ProductStateMatrix:
    """
    Make a product basis of all states using lexicographic order
    (similar to how numbers work with bases, like base 2 for spin 1/2)
    Every spin can have different states between -s_i and s_i totalling 2s_i + 1 states,
    which means there are (2s_1+1)*(2*s_2+1)*... product states,
    with every index from 0 to number_of_product_states - 1
    representing a unique product state.
    """

    def __init__(self, spin_values: list[number]):
        self.spin_values = spin_values
        self.number_of_spins = len(spin_values)
        self.number_of_single_spin_states = [int(2 * s + 1) for s in spin_values]
        self.number_of_product_states = self._calculate_number_of_states()
        self.nparray = self.generate_nparray()

    def _calculate_number_of_states(self) -> int:
        self.number_of_product_states = 1
        for number_states in self.number_of_single_spin_states:
            self.number_of_product_states *= number_states
        return self.number_of_product_states

    def generate_nparray(self) -> np.ndarray:
        matrix = np.empty([self.number_of_spins, self.number_of_product_states])
        for state in range(self.number_of_product_states):
            remainder = state
            for spin_index in range(self.number_of_spins):
                spin = self.spin_values[spin_index]
                number_of_single_spin_states = int(2 * spin + 1)
                matrix[spin_index, state] = (remainder % number_of_single_spin_states) - spin
                remainder //= number_of_single_spin_states
        return matrix

    # methods for easier access
    def __getitem__(self, *args, **kwargs):  # type: ignore
        return self.nparray.__getitem__(*args, **kwargs)  # type: ignore

    def spin(self, spin_index: int) -> SpinState:
        """
        Get the vector of the state of a single spin for every product state.
        The nth entry of the vector represents the state of the spin for product state n.
        """
        return SpinState(self.nparray[spin_index])

    def state(self, state_index: int) -> SpinState:
        """
        Get the vector with the states of all spins for a product state.
        The nth entry of the vector represents the state of the nth spin in this product state.
        """
        return SpinState(self.nparray[:, state_index].transpose())
