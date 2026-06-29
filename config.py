from typing import Any
from spin_ring import SpinRing
from math_helper import e_x, e_z


config: dict[str, Any] = { 


    "delete": {
        "range": "magnetic_field",
        "delete_beyond_range": True,
        "delete_all_temperatures": False
    },


    "calculate": {
        "spin_correlations": True,
        "spin_expectation_values": True,
        "toroidal_moment": True,
        "magnetization": True,
        "alignment": True,
    },


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
        "parameter_database": "./database/parameters.db",
        "results_folder": "./results",
    },


    "plot": {

        "number_of_shown_lowest_states": 9,
        "show_plots": True,
        "save_plots": False,
            
        "eigenvalues": {
            "generate_plots": True,
            "plots_to_generate": ["low", "all"],
            "y_limits": {"low": [], "all": []},
        },

        "toroidal_moment": {
            "generate_plots": False,
            "plots_to_generate": {
                "normal": ["x", "y", "z"],
                "thermal": ["x", "y", "z"],
            },
            "y_limits": {
                "normal": {"x": [], "y": [], "z": []},
                "thermal": {"x": [], "y": [], "z": []}
            },
        },

        "spin_correlation": {
            "generate_plots": False,
            "plots_to_generate": {
                "normal": ["1 2", "2 3", "3 1"],
                "thermal": ["1 2", "2 3", "3 1"],
            },
            "y_limits": {
                "normal": {"1 2": []},
                "thermal": {"1 2": []}
            },
        },

        "spin_expectation": {
            "generate_plots": False,
            "plots_to_generate": {
                "normal": ["1 x", "1 y", "1 z", "2 x", "2 y", "2 z"],
                "thermal": ["1 x", "1 y", "1 z", "2 x", "2 y", "2 z"],
            },
            "y_limits": {
                "normal": {"1 x": [], "1 y": [], "1 z": [], "2 x": [], "2 y": [], "2 z": []},
                "thermal": {"1 x": [], "1 y": [], "1 z": [], "2 x": [], "2 y": [], "2 z": []}
            }
        },

        "magnetization": {
            "generate_plots": False,
            "plots_to_generate": {
                "normal": ["x", "y", "z"],
                "thermal": ["x", "y", "z"],
            },
            "y_limits": {
                "normal": {"x": [], "y": [], "z": []},
                "thermal": {"x": [], "y": [], "z": []}
            },
        },

        "alignment": {
            "generate_plots": False,
            "plots_to_generate": {
                "normal": ["x", "y", "z"],
                "thermal": ["x", "y", "z"],
            },
            "y_limits": {
                "normal": {"x": [], "y": [], "z": []},
                "thermal": {"x": [], "y": [], "z": []}
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
