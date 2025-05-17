import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
import os
from .utilities import read_data, setup_plot, save_plot, get_default_colors, filter_energy_range

def plot_pdos(input_file:str, output_file: Optional[str] = None, pdos_type: str = "spdDOS", 
              emin: float = -10.0, emax: float = 10.0, colors: Optional[List[str]] = None, alpha: float = 0.8) -> None:
    """
    Plot the PDOS from the input file.
    
    Args:
        input_file (str): Path to the input file containing PDOS data.
        output_file (str, optional): Path to save the output plot. Default is None.
        pdos_type (str): Type of PDOS to plot. Options are 'spdDOS', 'totalDOS', or 'PDOS'.
        emin (float): Minimum energy for the plot.
        emax (float): Maximum energy for the plot.
        colors (List[str], optional): List of colors for the PDOS plot. Default is None.
        alpha (float): Transparency level for the PDOS plot. Default is 0.8.
    """

    if output_file is None:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = f"{base_name}_pdos.png"

    # Read data from the input file
    data = read_data(input_file, header=0, skip_first_row=True)
    filtered_data = filter_energy_range(data, 0, emin, emax)
    energy = filtered_data.iloc[:, 0].values

    # rest of the function remains the same...
    # set up the plot
    fig, ax = setup_plot("PDOS", "Energy (eV)", "PDOS (a. u./eV)")

    # define the plot configuration for different pdos types
    pdos_config = {
        'spdDOS': {
            'up_columns': [1, 3, 5],
            'down_columns': [2, 4, 6],
            'labels': ['s', 'p', 'd'],
            'fill': True
        },
        'totalDOS': {
            'up_columns': [1],
            'down_columns': [2],
            'labels': ['Total DOS'],
            'fill': True
        },
        'PDOS': {
            'up_columns':[1, 3, 5, 7, 9, 11, 13, 15, 17],
            'down_columns':[2, 4, 6, 8, 10, 12, 14, 16, 18],
            'labels': ['s', 'px', 'py', 'pz', 'dxy', 'dxz', 'dyz', 'dx2-y2', 'dz2'],
            'fill': True
        }
    }

    config = pdos_config[pdos_type]
    num_components = len(config['up_columns'])

    # get colors
    if colors is None:
        colors = get_default_colors(num_components)
    elif len(colors) < num_components:
        colors += get_default_colors(num_components - len(colors))

    # plot each component (up and down)
    for i, (up_col, down_col, label, color) in enumerate(zip(
            config['up_columns'], config['down_columns'], config['labels'], colors)):
        
        # plot the spin-up component
        up_dos = filtered_data.iloc[:, up_col].values
        line_up = ax.plot(energy, up_dos, label=label, color=color, alpha=alpha, linewidth=2, linestyle='-')[0]

        # plot the spin-down component
        down_dos = filtered_data.iloc[:, down_col].values
        line_down = ax.plot(energy, down_dos, label=f"{label} (down)", color=color, alpha=alpha, linewidth=2, linestyle='-')[0]

        # fill the area under the curve
        if config['fill']:
            # fill between the lines of spin up and down
            ax.fill_between(energy, up_dos, down_dos, where=(up_dos > down_dos), facecolor=color, alpha=alpha/2, interpolate=True)

        # add Fermi level line
        if emin<=0 <= emax:
            ax.axvline(x=0, color='black', linestyle='--', linewidth=1.5)
            ax.text(0.1, 0.9, 'Fermi Level', color='black', fontsize=10)

        # add horizontal line at y=0
        ax.axhline(y=0, color='black', linewidth=1)

        # set y-axis label to indicate spin direction
        ax.set_ylabel("PDOS (a. u./eV)")
        ax.set_xlabel("Energy (eV)")

        ax.legend()
        save_plot(fig, output_file)
        print(f"PDOS plot saved to {output_file}")