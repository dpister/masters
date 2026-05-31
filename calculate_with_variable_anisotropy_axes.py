import os

import numpy as np
from diagonalization_results import DiagonalizationResults
from math_helper import number

from hamiltonian import (
    get_anisotropy_hamiltonian_matrix,
    get_heisenberg_interaction_hamiltonian_matrix,
    get_zeeman_hamiltonian_matrix,
)
from parameter_database import NoRowFoundException, ParameterDatabase
from product_states import ProductStateMatrix
from spin import SpinRing
from config import config


def main():
    N: int = config["variables"]["number_of_spins_N"]
    s: number = config["variables"]["spin_s"]
    J: number = config["variables"]["heisenberg_interaction_constant_J"]
    D: number = config["variables"]["anisotropy_constant_D"]
    number_of_states = int(2 * s + 1) ** N
    x_start: number = config["variables"]["anisotropy_axes"]["range"]["start"]
    x_end: number = config["variables"]["anisotropy_axes"]["range"]["end"]
    number_of_steps = config["variables"]["anisotropy_axes"]["range"]["number_of_steps"]

    first_magnetic_field = config["variables"]["magnetic_field"]["single_value"][
        "magnetic_field_direction_of_first_spin"
    ]
    strength: number = config["variables"]["magnetic_field"]["single_value"]["strength"]
    magnetic_field_type: str = config["variables"]["magnetic_field"]["single_value"]["type"]

    spin_ring = SpinRing(
        number_of_spins=N,
        spin=s,
        heisenberg_interaction_constant=J,
        anisotropy_value=D,
        magnetic_field_of_first_spin=first_magnetic_field * strength,
        magnetic_field_type=magnetic_field_type,
    )

    data_folder: str = config["data_paths"]["folder"]
    os.makedirs(data_folder, exist_ok=True)
    parameter_db_path: str = config["data_paths"]["parameter_database"]

    parameter_id: int
    data_path: str
    saved_results: DiagonalizationResults

    with ParameterDatabase(os.path.join(data_folder, parameter_db_path)) as parameter_db:
        try:
            parameter_id = parameter_db.get_parameter_id(spin_ring)
        except NoRowFoundException:
            parameter_id = parameter_db.create_parameter_id(spin_ring)
            os.makedirs(os.path.join(data_folder, str(parameter_id)), exist_ok=True)
            diag_results_path: str = config["data_paths"]["npz_files"]["diagonalization_results"]
            data_path = os.path.join(
                data_folder, str(parameter_id), diag_results_path.format(parameter_id=parameter_id)
            )
            parameter_db.set_data_path(parameter_id, data_path)
            saved_results = DiagonalizationResults.new(length=0, number_of_states=number_of_states)
        else:
            data_path = parameter_db.get_npz_data_path(parameter_id)
            saved_results = DiagonalizationResults.load_from(data_path)

    product_state_matrix = ProductStateMatrix(number_of_spins=N, spin_value=s)
    hamiltonian = get_heisenberg_interaction_hamiltonian_matrix(spin_ring, product_state_matrix)
    hamiltonian += get_anisotropy_hamiltonian_matrix(spin_ring, product_state_matrix)

    new_x_values = np.linspace(x_start, x_end, number_of_steps)
    max_number_of_x_values = len(new_x_values) + len(saved_results)
    all_results = DiagonalizationResults.new(
        length=max_number_of_x_values, number_of_states=number_of_states
    )

    for x_value in new_x_values:
        #

        while saved_results.has_next() and saved_results.peek_x_value() < x_value:
            all_results.take_result_from(saved_results)

        if saved_results.has_next() and saved_results.peek_x_value() == x_value:
            all_results.take_result_from(saved_results)
            continue

        spin_ring.set_anisotropy_axes_for_all(angle_degrees=x_value)

        hamiltonian_zeeman = get_zeeman_hamiltonian_matrix(spin_ring, product_state_matrix)
        full_hamiltonian = hamiltonian + hamiltonian_zeeman
        eigenvalues, eigenvectors = np.linalg.eig(full_hamiltonian)
        if not np.all(np.isreal(eigenvalues)):
            raise Exception("Eigenvalues are complex")
        eigenvalues = np.real(eigenvalues)

        sort_eigenvalues_and_eigenvectors(eigenvalues, eigenvectors)

        all_results.append(
            x_value=x_value,
            eigenvalues=eigenvalues,
            eigenvectors=eigenvalues,
        )

    while saved_results.has_next():
        all_results.take_result_from(saved_results)

    all_results.save_to(data_path)


def sort_eigenvalues_and_eigenvectors(eigenvalues: np.ndarray, eigenvectors: np.ndarray) -> None:
    order = np.argsort(eigenvalues)
    eigenvalues[:] = eigenvalues[order]
    eigenvectors[:] = eigenvectors[:, order]


if __name__ == "__main__":
    main()
