import os
import datetime
from typing import Any
import numpy as np

from order import OrderGenerator
from config import config
from eigenvalue_plotter import EigenvaluePlotter
from math_helper import number
from parameter_database import ParameterDatabase
from plotter import Plotter
from results import Results
from spin_expectation_plotter import SpinExpectationPlotter
from spin_ring import SpinRing
from toroidal_moment_plotter import ToroidalMomentPlotter


def main():

    variables: dict[str, Any] = config["variables"]
    toggles = config["plot"]["toggles"]
    limits = config["plot"]["y_limits"]

    N: int = variables["number_of_spins_N"]
    s: number = variables["spin_s"]
    J: number = variables["heisenberg_interaction_constant_J"]
    D: number = variables["anisotropy_constant_D"]
    min_strength: number = variables["magnetic_field"]["range"]["start"]
    max_strength: number = variables["magnetic_field"]["range"]["end"]
    magnetic_field_direction = variables["magnetic_field"]["range"]["magnetic_field_direction_of_first_spin"]
    magnetic_field_type: str = variables["magnetic_field"]["range"]["type"]
    temperatures: list[number] = variables["temperatures"]

    anisotropy_axes_angle: number = variables["anisotropy_axes"]["single_value"]["angle"]

    x_label: str = variables["magnetic_field"]["range"]["x_axis_label"]
    magnetic_field_label: str = variables["magnetic_field"]["single_value"]["label_in_title"]
    title_subinfo: str = "für N={N}, s={s}, J={J}, {B}" + "\n" + "D={D}, Achsen in xy-Ebene"
    title_subinfo = title_subinfo.format(N=N, s=s, J=J, D=D, B=magnetic_field_label)

    spin_ring = SpinRing(
        number_of_spins=N,
        spin=s,
        heisenberg_interaction_constant=J,
        anisotropy_value=D,
        anisotropy_axis_angle=anisotropy_axes_angle,
        magnetic_field_direction_of_first_spin=magnetic_field_direction,
        magnetic_field_type=magnetic_field_type,
    )

    parameter_db_path: str = config["data"]["parameter_database"]
    results_folder: str = config["data"]["results_folder"]
    results_path_template: str = os.path.join(results_folder, "{parameter_id}.npz")
    images_folder: str = config["data"]["images_folder"]
    full_images_folder = os.path.join(images_folder, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    number_of_shown_states = config["plot"]["number_of_shown_lowest_states"]

    plotters: list[Plotter] = []
    eigenvalue_plotter = EigenvaluePlotter(
        number_of_shown_states=number_of_shown_states,
        xlabel=x_label,
        title_subinfo=title_subinfo,
        y_interval=limits["eigenvalues"]["all"],
        y_interval_low=limits["eigenvalues"]["low"],
    )
    spin_expectation_plotter = SpinExpectationPlotter(
        number_of_shown_states=number_of_shown_states,
        temperatures=temperatures,
        number_of_spins=N,
        xlabel=x_label,
        title_subinfo=title_subinfo,
        y_intervals=limits["spin_expectation"]["normal"],
        y_intervals_thermal=limits["spin_expectation"]["thermal"],
    )
    plotters.append(eigenvalue_plotter)
    plotters.append(spin_expectation_plotter)
    if toggles["should_plot_toroidal_moment"]:
        toroidal_moment_plotter = ToroidalMomentPlotter(
            number_of_shown_states=number_of_shown_states,
            temperatures=temperatures,
            xlabel=x_label,
            title_subinfo=title_subinfo,
            y_intervals=limits["toroidal_moment"]["normal"],
            y_intervals_thermal=limits["toroidal_moment"]["thermal"],
        )
        plotters.append(toroidal_moment_plotter)

    with ParameterDatabase(parameter_db_path) as parameter_db:
        entries = parameter_db.get_entries_by_magnetic_field_interval(
            spin_ring=spin_ring, min_magnetic_field=min_strength, max_magnetic_field=max_strength
        )

    number_of_x_values = len(entries)  # TODO
    number_of_states = spin_ring.product_state_matrix.number_of_product_states
    x_values = np.empty(number_of_x_values)
    all_eigenvalues = np.empty([number_of_x_values, number_of_states])
    all_eigenvectors = np.zeros([number_of_x_values, number_of_states, number_of_states]) * 0j
    all_spin_expectation_values = np.empty([number_of_x_values, number_of_states, N, 3]) * 0j
    spin_rings: list[SpinRing] = []

    for i, (parameter_id, strength) in enumerate(entries):
        #
        spin_ring.change_magnetic_field_strength(strength)
        spin_rings.append(spin_ring.get_copy())

        loaded_nparrays = np.load(results_path_template.format(parameter_id=parameter_id))
        eigenvalues = loaded_nparrays["eigenvalues"]
        eigenvectors = loaded_nparrays["eigenvectors"]
        spin_expectation_values = loaded_nparrays["spin_expectation_values"]
        x_values[i] = strength
        all_eigenvalues[i] = eigenvalues
        all_eigenvectors[i] = eigenvectors
        all_spin_expectation_values[i] = spin_expectation_values

    results = Results(
        spin_rings=spin_rings,
        product_state_matrix=spin_ring.product_state_matrix,
        x_values=x_values,
        eigenvalues=all_eigenvalues,
        eigenvectors=all_eigenvectors,
        temperatures=temperatures,
        spin_expectation_values=all_spin_expectation_values,
    )
    results.sort()

    print(results.eigenvectors[0])
    order = OrderGenerator(x_values=results.x_values, eigenvalues=results.eigenvalues)
    state_ordering_matrix = order.calculate_state_order_using_interpolation()

    for plotter in plotters:
        plotter.add_points(
            results=results,
            color_map=state_ordering_matrix,
        )

    import matplotlib.pyplot as plt

    plt.show()  # type: ignore

    if toggles["should_save_plots"]:
        os.makedirs(full_images_folder)
        for plotter in plotters:
            plotter.save(full_images_folder)


if __name__ == "__main__":
    main()
