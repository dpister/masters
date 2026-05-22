

from typing import Any

import numpy as np   
from math_helper import number


class SpinState:

    def __init__(self, array: np.ndarray):
        self.array = np.copy(array)

    def changed(self, ind: int, shift: int) -> SpinState:
        """
        Returns a copy of the state with the entry at the index shifted.
        Simplifies comparison of states and an easy implementation of kronecker delta
        """
        copy = np.copy(self.array)
        copy[ind] += shift
        return SpinState(copy)
    
    def __eq__(self, obj: Any) -> bool:
        if not isinstance(obj, SpinState): return False
        return np.array_equal(self.array, obj.array)
    
    def __getitem__(self, index: int) -> number:
        return self.array[index]
    

class ProductStateMatrix:
    """
    Make a product basis of all states using lexicographic order 
    (similar to how numbers work with bases, like base 2 for spin 1/2)
    Every spin can have different states between -s and s totalling 2s + 1 states, 
    which means there are (2s+1)^N product states, 
    with every index from 0 to number_of_states - 1
    representing a unique product state.
    """

    def __init__(self, number_of_spins: int, spin_value: number):
        self.number_of_spins = number_of_spins
        self.spin_value = spin_value
        self.product_state_matrix = self.generate_product_state_matrix(number_of_spins, spin_value)

    def generate_product_state_matrix(self, number_of_spins: int, spin: number) -> np.ndarray:
        s = spin
        N = number_of_spins
        b = int(2*s+1)
        number_of_states = int(2*s + 1)**N
        matrix = -s * np.ones([number_of_spins, number_of_states])
        
        for x in range(b**N):
            xsave=x
            ind=0                            
            while x:
                matrix[ind, xsave]=int(x % b)-s
                x //= b
                ind+=1
        return matrix
    
    # methods for easier access
    def __getitem__(self, *args, **kwargs): #type: ignore
        return self.product_state_matrix.__getitem__(*args, **kwargs) #type: ignore
    
    def spin(self, spin_index: int) -> SpinState:
        """
        Get the vector of the state of a single spin for every product state.
        The nth entry of the vector represents the state of the spin for product state n.
        """
        return SpinState(self.product_state_matrix[spin_index])
    
    def state(self, state_index: int) -> SpinState:
        """
        Get the vector with the states of all spins for a product state.
        The nth entry of the vector represents the state of the nth spin in this product state.
        """
        return SpinState(self.product_state_matrix[:, state_index].transpose())
        