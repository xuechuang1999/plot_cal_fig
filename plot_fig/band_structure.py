import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from typing import Optional, List
from .utilities import read_data, setup_plot, save_plot, get_default_colors, setup_plot_band_structure

def plot_band_structure(input_file: str, output_file: str = 'band.png',
                       direction: str = 'z', below_fermi: float = 5.0,
                       above_fermi: float = 5.0, colors: Optional[List[str]] = None,
                       show: bool = False):
    """Plot electronic band structure from VASP output files.
    
    Args:
        input_file: Path to EIGENVAL file
        output_file: Output image filename
        direction: High symmetry direction ('x', 'y', or 'z')
        below_fermi: Energy range below Fermi level (eV)
        above_fermi: Energy range above Fermi level (eV)
        colors: List of colors for each spin channel
        show: Whether to show interactive plot
    """
    # Read Fermi energy and nspin from OUTCAR
    outcar_file = input_file.replace('EIGENVAL', 'OUTCAR')
    try:
        with open(outcar_file, 'r') as f:
            outcar_content = f.readlines()
    except IOError:
        raise IOError(f"Cannot read OUTCAR file at {outcar_file}")

    # Parse OUTCAR
    nspin, efermi = parse_outcar(outcar_content)
    
    # Read eigenvalues from EIGENVAL
    kpts, eig = parse_eigenval(input_file, nspin)
    eig -= efermi  # Shift to Fermi level
    
    # Determine direction index
    directions = {'x': 0, 'y': 1, 'z': 2}
    dir_idx = directions[direction]
    
    # Set up plot
    fig, ax = setup_plot_band_structure("Band Structure", "k-points", r"$E - E_F$ (eV)")
    
    # Set colors
    if colors is None:
        colors = ['r', 'b'] if nspin == 2 else ['k']
    
    # Plot bands
    for ispin in range(nspin):
        for ib in range(eig.shape[0]):
            ax.plot(kpts[:, dir_idx], eig[ib, :, ispin], 
                   color=colors[ispin], linewidth=1, alpha=0.8)
    
    # Add Fermi level and grid
    ax.axhline(0, color='k', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # Set axis limits and labels
    ax.set_xlim([kpts[0, dir_idx], kpts[-1, dir_idx]])
    ax.set_ylim([-below_fermi, above_fermi])
    
    # Add high symmetry points labels
    add_symmetry_labels(ax, kpts[:, dir_idx])

    # Save or show plot
    if show:
        plt.show()
    else:
        save_plot(fig, output_file)

def parse_outcar(content: List[str]) -> tuple:
    """Parse OUTCAR content to get nspin and Fermi energy."""
    nspin, efermi = 1, 0.0
    for line in content:
        if line.startswith('   ISPIN'):
            nspin = int(line.split()[2])
        elif line.startswith(' E-fermi'):
            efermi = float(line.split()[2])
            break
    return nspin, efermi

def parse_eigenval(filename: str, nspin: int) -> tuple:
    """Parse EIGENVAL file to get kpoints and eigenvalues."""
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    # Skip header
    for i in range(5):
        lines.pop(0)
    
    # Read number of kpoints and bands
    nk, nb = map(int, lines.pop(0).split()[1:3])
    
    kpts = np.zeros((nk, 3))
    eig = np.zeros((nb, nk, nspin))
    
    for ik in range(nk):
        lines.pop(0)  # Skip empty line
        kpts[ik] = list(map(float, lines.pop(0).split()[:3]))
        for ib in range(nb):
            parts = list(map(float, lines.pop(0).split()))
            eig[ib, ik] = parts[1:1+nspin]
    
    return kpts, eig

def add_symmetry_labels(ax, kpoints):
    """Add high symmetry point labels to the plot."""
    # This is a simplified version - you may need to customize based on your system
    ax.set_xticks([kpoints[0], kpoints[-1]])
    ax.set_xticklabels([r'$\Gamma$', r'$X$'])
    
    # Add minor ticks
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))