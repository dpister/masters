import os
from typing import Any

import numpy as np
from math_helper import is_almost_real, number, sort_eigenvalues_and_eigenvectors

from hamiltonian import (
    get_anisotropy_hamiltonian_matrix,
    get_heisenberg_interaction_hamiltonian_matrix,
    get_zeeman_hamiltonian_matrix,
)
from parameter_database import NoRowFoundException, ParameterDatabase
from spin_expectation_value import calculate_spin_expectation_value
from spin_ring import SpinRing
from config import config


def main():
    variables: dict[str, Any] = config["variables"]
    N: int = variables["number_of_spins_N"]
    s: number = variables["spin_s"]
    J: number = variables["heisenberg_interaction_constant_J"]
    D: number = variables["anisotropy_constant_D"]
    magnetic_field_start: number = variables["magnetic_field"]["range"]["start"]
    magnetic_field_end: number = variables["magnetic_field"]["range"]["end"]
    number_of_steps = variables["magnetic_field"]["range"]["number_of_steps"]
    anisotropy_axis_angle = variables["anisotropy_axes"]["single_value"]["angle"]

    magnetic_field_direction = variables["magnetic_field"]["range"]["magnetic_field_direction_of_first_spin"]
    magnetic_field_type: str = config["variables"]["magnetic_field"]["range"]["type"]

    spin_ring = SpinRing(
        number_of_spins=N,
        spin=s,
        heisenberg_interaction_constant=J,
        anisotropy_value=D,
        anisotropy_axis_angle=anisotropy_axis_angle,
        magnetic_field_type=magnetic_field_type,
        magnetic_field_direction_of_first_spin=magnetic_field_direction,
    )

    hamiltonian = get_heisenberg_interaction_hamiltonian_matrix(
        product_state_matrix=spin_ring.product_state_matrix,
        heisenberg_interaction_matrix=spin_ring.heisenberg_interaction_matrix,
    )
    hamiltonian += get_anisotropy_hamiltonian_matrix(
        spins=spin_ring.spins, product_state_matrix=spin_ring.product_state_matrix
    )

    strengths = np.linspace(magnetic_field_start, magnetic_field_end, number_of_steps)

    results_folder: str = config["data"]["results_folder"]
    os.makedirs(results_folder, exist_ok=True)
    parameter_db_path: str = config["data"]["parameter_database"]
    results_path_template: str = os.path.join(results_folder, "{parameter_id}.npz")

    for strength in strengths:
        #

        spin_ring.change_magnetic_field_strength(strength)

        parameter_id: int
        with ParameterDatabase(parameter_db_path) as parameter_db:
            try:
                parameter_id = parameter_db.get_parameter_id(spin_ring)
                if os.path.exists(results_path_template.format(parameter_id=parameter_id)):
                    continue
            except NoRowFoundException:
                pass
            parameter_id = parameter_db.create_parameter_id(spin_ring)

        hamiltonian_zeeman = get_zeeman_hamiltonian_matrix(
            spins=spin_ring.spins, product_state_matrix=spin_ring.product_state_matrix
        )

        full_hamiltonian = hamiltonian + hamiltonian_zeeman
        eigenvalues, eigenvectors = np.linalg.eig(full_hamiltonian)
        if not is_almost_real(eigenvalues):
            raise Exception("Eigenvalues are complex")
        eigenvalues = np.real(eigenvalues)

        sort_eigenvalues_and_eigenvectors(eigenvalues, eigenvectors)

        number_of_states = spin_ring.product_state_matrix.number_of_product_states
        spin_expectation_values = np.empty([number_of_states, N, 3]) * 0j

        for state in range(number_of_states):
            for spin in range(N):
                spin_expectation_value = calculate_spin_expectation_value(
                    spin_index=spin,
                    eigenvalue_index=state,
                    product_state_matrix=spin_ring.product_state_matrix,
                    eigenvectors=eigenvectors,
                )
                spin_expectation_values[state, spin] = spin_expectation_value

        np.savez(
            results_path_template.format(parameter_id=parameter_id),
            eigenvalues=eigenvalues,
            eigenvectors=eigenvectors,
            spin_expectation_values=spin_expectation_values,
        )


if __name__ == "__main__":
    main()
