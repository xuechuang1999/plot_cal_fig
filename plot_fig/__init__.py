# -*- coding: utf-8 -*-
from .band_structure import plot_band_structure
from .pdos import plot_pdos
from .delta_G import plot_delta_G


__name__ = "plot_fig"
__version__ = "0.0.0"
__author__ = "chxue"
__email__ = "ch.xue99@gmail.com"
__description__ = 'Plot the PDOS and band structure of DFT calculation results'
__license__ = 'GPLv3'
__url__ = '../README.md'
__epilog__ = 'The current version (v' + __version__ + ') may contain bugs. To get the latest version, please run:\
\n\n\t$ pip3 install --upgrade plot_fig\n\nWe also recommend you to see the documentation at:\
\n\n\t' + __url__ + '\n\n\
You are also welcome to contact me at ' + __email__ + ' for any questions, feedbacks or comments.'

__all__ = [
    "plot_band_structure",
    "plot_pdos",
    "plot_delta_G"
]