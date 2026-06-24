from typing import Any
from spin_ring import SpinRing
from math_helper import e_x, e_z


config: dict[str, Any] = { 

    "variables": {

        "number_of_spins_N": 2,                            
        "spin_s": 1,                             
        "heisenberg_interaction_constant_J": 1,
        "anisotropy_constant_D": -4,
        "temperatures": [1,2,4,8],

        "magnetic_field": {
            "single_value": {
                "strength": 3, 
                "magnetic_field_direction_of_first_spin": e_z, 
                "type": SpinRing.MagneticFieldType.linear.value,
                "label_in_title": r"$B^z=3$T",
            },
            "range": {
                "magnetic_field_direction_of_first_spin": e_x, 
                "type": SpinRing.MagneticFieldType.circular.value,
                "start": -2,
                "end": 2,
                "number_of_steps": 2001,
                "x_axis_label": r"$B^\varphi$ in T",
                "label_in_title": r"$\vec(B)=B\vec{e}^\varphi$",
                "label_order_x_value": 0,
            },
            "spacial_average": {} # TODO
        },

        "anisotropy_axes": {
            "single_value": {
                "angle": 0,
            },
            "range": {
                "start": 0,
                "end": 90,
                "number_of_steps": 91,
                "x_axis_label": r"$\varphi$ in $^\circ$",
                "label_order_x_value": None,
            }
        },
    },

    "data": {
        "images_folder": "./images",
        "parameter_database": "./parameters.db",
        "results_folder": "./results",
    },

    "plot": {
            
        "toggles": {
            "should_save_plots": False,
            "should_plot_eigenvalues": True,
            "should_plot_all_eigenvalues": True,
            "should_plot_spin_correlations": True,
            "should_plot_spin_expectation_values": True,
            "should_plot_toroidal_moment": False,
            "should_plot_magnetization": True,
            "should_disable_color_coding_for_lowest_eigenvalues": False
        },

        "number_of_shown_lowest_states": 9,

        
        "y_limits": {
            "eigenvalues": {
                "low": [],
                "all": []
            },
            "toroidal_moment": {
                "normal": {"x": [-3,3], "y": [-3,3], "z": [-3, 3]},
                "thermal": {"x": [-3,3], "y": [-3,3], "z": [-3, 3]},
            },
            "spin_correlation": {
                "normal": [],
                "thermal": []
            },
            "spin_expectation": {
                "normal": {"x": [-3,3], "y": [-3,3], "z": [-3, 3]},
                "thermal": {"x": [], "y": [], "z": []},
            },
            "magnetization": {
                "x": [-3,3], "y": [-3,3], "z": [-3, 3]
            },
        },

        "spin_correlation": {
            "normal": {
                "y_interval": [],
                "ylabel": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>_\\nu$",
                "title": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": [],
                "ylabel": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>(T)$",
                "title": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
        
        "magnetization": {
            "thermal": {
                "y_interval": {"x": [-2,2], "y": [-2,2], "z": [-2, 2]},
                "ylabel": "$<\\mathcal{{M}}^{direction}>(T)$ in J/K",
                "title": "$<\\mathcal{{M}}^{direction}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
    },


    "paths": {

        "images": {
            "lowest_eigenvalues": "low_eigenvalues.png",
            "all_eigenvalues": "all_eigenvalues.png",
            "spin_expectation": "spin{spin_direction}_spin_expval.png",
            "spin_expectation_thermal": "spin{spin_direction}_spin_thermal_expval.png",
            "spin_correlation": "spin{spin1_ind}_spin{spin2_ind}_correlation_expval.png",
            "spin_corr_thermal": "spin{spin1_ind}_spin{spin2_ind}_correlation_thermal_expval.png",
            "magnetization": "M{direction}_magnetization_expval.png",
            "magnetization_thermal": "M{direction}_magnetization_thermal_expval.png",
        },

    }
}
