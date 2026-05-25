from spin import SpinRing


config = { # type: ignore

    "toggles": {
        "should_save_plots": True,
        "should_use_variable_magnetic_field": True,
        "should_use_variable_anisotropy_axes": True,
        "should_compute_spin_correlations": True,
        "should_compute_spin_expectation_values": True,
        "should_compute_toroidal_moment": True,
        "should_compute_magnetization": True,
        "should_only_plot_lowest_eigenvalues": False,
        "should_use_special_color_coding": True
    },

    "variables": {
        
        "number_of_spins_N": 2,                            
        "spin_s": 3/2,                             
        "heisenberg_interaction_constants_J": [1],
        "anisotropy_constants_D": [-1],
        "first_anisotropy_axis_dir": [1,0,0],
        # if the magnetic field is circular,
        # define the magnetic field of the first spin
        "magnetic_field_dir": [0,0,1], 
        "magnetic_field_type": "linear",
        "temperatures": [1,2,4,8],

        "variable_magnetic_field": {
            "type": SpinRing.MagneticFieldType.circular.value,
            "start": -3,
            "finish": 3,
            "number_of_steps": 500,
        },

        "variable_anisotropy_axes": {
            "start_angle": 0,
            "finish_angle": 90,
            "number_of_steps": 181,
        },

        "eigenvalues": {
            "number_of_lowest_states": 6,
        },

        "magnetization": {
            "directions": ["x", "y", "z"],
                                            
        },

        "toroidal_moment": {
            "directions": ["x", "y", "z"],
        },
    },


    "plot": {

        "legendsize": 13,
        "ticksize": 12,
        "labelsize": 15,
        "linewidth": 0.000001,
        "marker": ".",
        "default_color": "blue",
        "bbox_inches": 'tight', # TODO figure out what the hell this is
        "label_location": "upper right",

        "temperature_label": "$T=${temperature} K",
        "nu_label": "$\nu=${eigenvalue_index}",

        "colors": ['red', 'blue', 'green', 'purple', 'orange', 'turquoise', 'magenta', 'brown', 'grey'],
        "color_swap": 0.1, # when eigenvalues reach closer than this threshhold it is considered a level crossing
        "color_degen": 0.0001, # eigenvalues closer than this number are considered degenerate
        
        "lowest_eigenvalues": {
            "y_interval": (),
            "ylabel": r'$E_\nu$ in K',
            "title": "Unterste Eigenwerte $E_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",
        },

        "eigenvalues": {
            "y_interval": (),
            "ylabel": r'$E_\nu$ in K',
            "title": "Eigenwerte $E_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
        },
        
        "toroidal_moment": {
            "normal": {
                "y_interval": {"x": (-2.5,2.5), "y": (-2.5,2.5), "z": (-5.5, 5.5)},
                "ylabel": '$<\\hat{{\\tau}}{direction}x>_\\nu$ in a.u.',
                "title": "$<\\hat{{\\tau}}^{direction}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": {"x": (), "y": (), "z": ()},
                "ylabel": '$<\\hat{{\\tau}}^{direction}>(T)$ in a.u.',
                "title": "$<\\hat{{\\tau}}^{direction}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
        
        "spin_expectation": {
            "normal": {
                "y_interval": {"x": (-3,3), "y": (-3,3), "z": (-3, 3)},
                "ylabel": "$<\\hat{{s}}^{direction}_{spin_index}>_\\nu$",
                "title": "$<\\hat{{\\s}}^{direction}_{spin_index}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": (-2.5,2.5),
                "ylabel": "$<\\hat{{s}}^{direction}_{spin_index}>(T)$",
                "title": "$<\\hat{{s}}^{direction}_{spin_index}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
        
        "spin_correlation": {
            "normal": {
                "y_interval": (),
                "ylabel": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>_\\nu$",
                "title": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>_\\nu$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
            "thermal": {
                "y_interval": (),
                "ylabel": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>(T)$",
                "title": "$<\\hat{{\\vec{{s}}}_{spin1_index}\\cdot\\hat{{\\vec{{s}}}}_{spin2_index}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },
        
        "magnetization": {
            "thermal": {
                "y_interval": {"x": (-2,2), "y": (-2,2), "z": (-2, 2)},
                "ylabel": "$<\\mathcal{{M}}^{direction}>(T)$ in J/K",
                "title": "$<\\mathcal{{M}}^{direction}>(T)$ für N={N}, s={s}, J={J} K, D={D} K, $\\vec{{B}}=${B}",            
            },
        },

        "variable_magnetic_field": {
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

    "file_paths_for_saving": {

        "images": {
            "lowest_eigenvalues": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_low_eigvals.png",
            "all_eigenvalues": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_all_eigvals_.png",
            "toroidal_moment": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_T{toroidal_direction}_tor_moment_expval.png",
            "toroidal_moment_thermal": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_T{toroidal_direction}_tor_moment_expval_thermal.png",
            "spin_expectation": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_spin{spin_direction}_spin_expval.png",
            "spin_expectation_thermal": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_spin{spin_direction}_spin_thermal_expval.png",
            "spin_correlation": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_spin{spin1_ind}_spin{spin2_ind}_correl_expval.png",
            "spin_corr_thermal": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_spin{spin1_ind}_spin{spin2_ind}_correl_thermal_expval.png",
            "magnetization": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_M{direction}_magnet_expval.png",
            "magnetization_thermal": "s{s}_J{J}_D{D}_{B_type}_{B_interval}_M{direction}_magnet_thermal_expval.png",
        },

        "data": {},
    }
}
