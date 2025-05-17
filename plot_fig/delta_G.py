import matplotlib.pyplot as plt
from .utilities import read_data, setup_plot, save_plot

def plot_delta_G(input_file: str, output_file: str = 'deltaG.png'):
    """Plot delta G versus reaction coordinate."""
    
    # Read data
    data = read_data(input_file)
    rc = data.iloc[:, 0].values  # Reaction coordinate
    dG = data.iloc[:, 1].values  # Delta G
    
    # Set up plot
    fig, ax = setup_plot("Reaction Energy Profile", "Reaction Coordinate", "ΔG (eV)")
    
    # Plot the energy profile
    ax.plot(rc, dG, 'b-', linewidth=2, marker='o', markersize=8)
    
    # Highlight important points
    ax.scatter(rc[0], dG[0], color='g', s=100, label='Reactant')
    ax.scatter(rc[-1], dG[-1], color='r', s=100, label='Product')
    
    # Find and label transition state
    ts_idx = dG.argmax()
    ax.scatter(rc[ts_idx], dG[ts_idx], color='m', s=100, label='Transition State')
    
    ax.legend()
    save_plot(fig, output_file)