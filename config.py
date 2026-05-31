from typing import Any
from spin import SpinRing
from math_helper import e_x, e_z


config: dict[str, Any] = { 

    "toggles": {
        "should_save_plots": True,
        "should_compute_spin_correlations": True,
        "should_compute_spin_expectation_values": True,
        "should_compute_toroidal_moment": True,
        "should_compute_magnetization": True,
        "should_only_plot_lowest_eigenvalues": False,
        "should_disable_color_coding_for_lowest_eigenvalues": False
    },

    "variables": {

        "number_of_spins_N": 2,                            
        "spin_s": 1/2,                             
        "heisenberg_interaction_constant_J": 1,
        "anisotropy_constant_D": -1,
        "temperatures": [1,2,4,8],

        "magnetic_field": {
            "single_value": {
                "strength": 3, 
                "magnetic_field_direction_of_first_spin": e_z, 
                "type": SpinRing.MagneticFieldType.linear.value,
            },
            "range": {
                "magnetic_field_direction_of_first_spin": e_x, 
                "type": SpinRing.MagneticFieldType.circular.value,
                "start": -3,
                "end": 3,
                "number_of_steps": 500,
            }
        },

        "anisotropy_axes": {
            "single_value": {
                "angle": 0,
            },
            "range": {
                "start": -50,
                "end": 200,
                "number_of_steps": 400,
            }
        },
    },


    "plot": {

        "number_of_shown_lowest_states": 6,

        "legendsize": 13,
        "ticksize": 12,
        "labelsize": 15,
        "linewidth": 0.000001,
        "marker": ".",
        "default_color": "blue",
        "should_trim_whitespace_around_plot": True, 
        "legend_location": "upper right",

        "temperature_label": "$T=${temperature} K",
        "nu_label": "$\nu=${eigenvalue_index}",

        "colors": ['red', 'blue', 'green', 'purple', 'orange', 'turquoise', 'magenta', 'brown', 'grey'],
        "color_swap": 0.1, # when eigenvalues reach closer than this threshhold it is considered a level crossing
        "color_degen": 0.0001, # eigenvalues closer than this number are considered degenerate
        
        "lowest_eigenvalues": {
            "y_interval": [],
            "ylabel": r'$E_\nu$ in K',
            "title": "Unterste Eigenwerte $E_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",
        },

        "eigenvalues": {
            "y_interval": [],
            "ylabel": r'$E_\nu$ in K',
            "title": "Eigenwerte $E_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
        },
        
        "toroidal_moment": {
            "normal": {
                "y_interval": {"x": [-2.5,2.5], "y": [-2.5,2.5], "z": [-5.5, 5.5]},
                "ylabel": '$<\\hat{{\\tau}}{direction}x>_\\nu$ in a.u.',
                "title": "$<\\hat{{\\tau}}^{direction}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": {"x": [], "y": [], "z": []},
                "ylabel": '$<\\hat{{\\tau}}^{direction}>(T)$ in a.u.',
                "title": "$<\\hat{{\\tau}}^{direction}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
        
        "spin_expectation": {
            "normal": {
                "y_interval": {"x": [-3,3], "y": [-3,3], "z": [-3, 3]},
                "ylabel": "$<\\hat{{s}}^{direction}_{spin_index}>_\\nu$",
                "title": "$<\\hat{{\\s}}^{direction}_{spin_index}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": [-2.5,2.5],
                "ylabel": "$<\\hat{{s}}^{direction}_{spin_index}>(T)$",
                "title": "$<\\hat{{s}}^{direction}_{spin_index}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
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

        "magnetic_field_range": {
            "linear": {
                "xlabel": r'$B^z$ in T',
                "name_in_title": r'$\vec{B}^z$'
            },
            "circular": {
                "xlabel": r'$B^\varphi$ in T',
                "name_in_title": r'$\vec{B}^\varphi$',
            },
        },

        "anisotropy_axes_range": { # TODO
            "linear": {
                "xlabel": r'$B^z$ in T',
                "name_in_title": r'$\vec{B}^z$'
            },
            "circular": {
                "xlabel": r'$B^\varphi$ in T',
                "name_in_title": r'$\vec{B}^\varphi$',
            }

        },
    },

    "data_paths": {

        "folder": "./data",
        "parameter_database": "parameters.db",

        "images": {
            "lowest_eigenvalues": "{parameter_id}_low_eigenvalues.png",
            "all_eigenvalues": "{parameter_id}_all_eigenvalues_.png",
            "toroidal_moment": "{parameter_id}_T{toroidal_direction}_tor_moment_expval.png",
            "toroidal_moment_thermal": "{parameter_id}_T{toroidal_direction}_tor_moment_expval_thermal.png",
            "spin_expectation": "{parameter_id}_spin{spin_direction}_spin_expval.png",
            "spin_expectation_thermal": "{parameter_id}_spin{spin_direction}_spin_thermal_expval.png",
            "spin_correlation": "{parameter_id}_spin{spin1_ind}_spin{spin2_ind}_correlation_expval.png",
            "spin_corr_thermal": "{parameter_id}_spin{spin1_ind}_spin{spin2_ind}_correlation_thermal_expval.png",
            "magnetization": "{parameter_id}_M{direction}_magnetization_expval.png",
            "magnetization_thermal": "{parameter_id}_M{direction}_magnetization_thermal_expval.png",
        },

        "npz_files": {
            "diagonalization_results": "{parameter_id}_diag_results.npz",
        }

    }
}
