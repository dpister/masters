import os
from typing import Any

from math_helper import number
from parameter_database import ParameterDatabase
from spin_ring import SpinRing
from config import config


def main():
    variables: dict[str, Any] = config["variables"]
    delete_config: dict[str, Any] = config["delete"]

    range_to_delete: str = delete_config["range"]
    delete_beyond_range: bool = delete_config["delete_beyond_range"]

    spin_ring = build_spin_ring(variables, range_to_delete)

    parameter_db_path: str = config["data"]["parameter_database"]
    results_folder: str = config["data"]["results_folder"]
    results_path_template: str = os.path.join(results_folder, "{parameter_id}.npz")

    with ParameterDatabase(parameter_db_path) as parameter_db:
        entries = get_entries_to_delete(parameter_db, spin_ring, variables, range_to_delete, delete_beyond_range)
        parameter_ids = [parameter_id for parameter_id, _ in entries]

        if not parameter_ids:
            print("No matching entries found, nothing to delete")
            return

        print(f"About to delete {len(parameter_ids)} entries (and their result files) from the database")
        confirmation = input("Type 'yes' to confirm: ")
        if confirmation != "yes":
            print("Aborted, nothing was deleted")
            return

        delete_result_files(parameter_ids, results_path_template)
        parameter_db.delete_parameters(parameter_ids)

    print(f"Deleted {len(parameter_ids)} entries")


def build_spin_ring(variables: dict[str, Any], range_to_delete: str) -> SpinRing:
    N: int = variables["number_of_spins_N"]
    s: number = variables["spin_s"]
    J: number = variables["heisenberg_interaction_constant_J"]
    D: number = variables["anisotropy_constant_D"]

    if range_to_delete == "magnetic_field":
        return SpinRing(
            number_of_spins=N,
            spin=s,
            heisenberg_interaction_constant=J,
            anisotropy_value=D,
            anisotropy_axis_angle=variables["anisotropy_axes"]["single_value"]["angle"],
            magnetic_field_direction_of_first_spin=variables["magnetic_field"]["range"][
                "magnetic_field_direction_of_first_spin"
            ],
            magnetic_field_type=variables["magnetic_field"]["range"]["type"],
        )
    elif range_to_delete == "anisotropy_axes":
        return SpinRing(
            number_of_spins=N,
            spin=s,
            heisenberg_interaction_constant=J,
            anisotropy_value=D,
            magnetic_field_direction_of_first_spin=variables["magnetic_field"]["single_value"][
                "magnetic_field_direction_of_first_spin"
            ],
            magnetic_field_strength=variables["magnetic_field"]["single_value"]["strength"],
            magnetic_field_type=variables["magnetic_field"]["single_value"]["type"],
        )
    else:
        raise ValueError(f'Unknown delete range "{range_to_delete}", expected "magnetic_field" or "anisotropy_axes"')


def get_entries_to_delete(
    parameter_db: ParameterDatabase,
    spin_ring: SpinRing,
    variables: dict[str, Any],
    range_to_delete: str,
    delete_beyond_range: bool,
) -> list[tuple[int, number]]:
    if range_to_delete == "magnetic_field":
        if delete_beyond_range:
            return parameter_db.get_entries_matching_magnetic_field_fixed_parameters(spin_ring)
        return parameter_db.get_entries_by_magnetic_field_interval(
            spin_ring=spin_ring,
            min_magnetic_field=variables["magnetic_field"]["range"]["start"],
            max_magnetic_field=variables["magnetic_field"]["range"]["end"],
        )
    else:
        if delete_beyond_range:
            return parameter_db.get_entries_matching_anisotropy_axes_fixed_parameters(spin_ring)
        return parameter_db.get_entries_by_angle_interval(
            min_angle=variables["anisotropy_axes"]["range"]["start"],
            max_angle=variables["anisotropy_axes"]["range"]["end"],
            spin_ring=spin_ring,
        )


def delete_result_files(parameter_ids: list[int], results_path_template: str) -> None:
    for parameter_id in parameter_ids:
        result_path = results_path_template.format(parameter_id=parameter_id)
        if os.path.exists(result_path):
            os.remove(result_path)


if __name__ == "__main__":
    main()
