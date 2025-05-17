import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import List, Optional


def read_data(file_path: str, header: Optional[int] = None, skip_first_row: bool = False) -> pd.DataFrame:
    """
    Read data from a file and return it as a pandas DataFrame.
    
    Args:
        file_path (str): Path to the data file.
        header (int, optional): Row number(s) to use as the column names. Default is None.
        
    Returns:
        pd.DataFrame: DataFrame containing the data from the file.
    """
    try:
        skiprows = 1 if skip_first_row else 0
        data = pd.read_csv(file_path, delim_whitespace=True, header=header, comment="#", delimiter="\t", skiprows=skiprows)
        return data
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        # return pd.DataFrame()

def setup_plot(title: str, xlabel: str, ylabel:str) -> plt.Figure:
    """
    Set up the plot with title and labels.
    
    Args:
        title (str): Title of the plot.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        
    Returns:
        plt.Figure: Figure object for the plot.
    """
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return fig

def setup_plot_band_structure(title: str, xlabel: str, ylabel: str) -> tuple:
    """Set up a matplotlib figure with common settings.
    
    Returns:
        tuple: (fig, ax) matplotlib Figure and Axes objects
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, linestyle='--', alpha=0.6)
    return fig, ax

def save_plot(fig: plt.Figure, output_file: str) -> None:
    """
    Save the plot to a file.
    
    Args:
        fig (plt.Figure): Figure object to save.
        output_file (str): Path to the output file.
    """
    fig.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)

def get_default_colors(num_colors: int) -> List[str]:
    """
    Get a list of default colors for plotting.
    
    Args:
        num_colors (int): Number of colors needed.
        
    Returns:
        List[str]: List of color codes.
    """
    # default_colors = ["#fdebaa", "#edc3a5", "#dbe4fb", "#abd1bc", "#e3bbed", "#cccc99", 
    #                   "#bed0f9", "#fcb6a5", "#f1f1f1"]
    camp = plt.get_cmap("tab10")
    default_colors = [camp(i % 10) for i in range(num_colors)]
    return default_colors

def filter_energy_range(data: pd.DataFrame, energy_col: int, emin: float, emax: float) -> pd.DataFrame:
    """
    Filter the data based on energy range.
    
    Args:
        data (pd.DataFrame): DataFrame containing the data.
        energy_col (int): Column index for energy values.
        emin (float): Minimum energy value.
        emax (float): Maximum energy value.
        
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    return data[(data.iloc[:, energy_col] >= emin) & (data.iloc[:, energy_col] <= emax)]

def validate_file(file_path: str, expected_name: Optional[str] = None) -> None:
    """Validate that file exists and has expected name pattern."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if expected_name and expected_name not in os.path.basename(file_path):
        raise ValueError(f"File name should contain '{expected_name}'")