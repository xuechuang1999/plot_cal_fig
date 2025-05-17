import argparse
from . import plot_band_structure, plot_pdos, plot_delta_G

def main():
    parser = argparse.ArgumentParser(description="Plotting tools for DFT calculation results.")
    subparsers = parser.add_subparsers(dest="menu", help="Select plot type", required=True)

    # band structure parser
    # band_parser = subparsers.add_parser("band", help="Plot band structure")
    # band_parser.add_argument("input_file", type=str, help="The data file of band structure")
    # band_parser.add_argument("--output", type=str, help="The output file for band structure", default="band_structure.png")
    # band_parser.add_argument("--emin", type=float, help="Minimum energy for band structure", default=-10.0)
    # band_parser.add_argument("--emax", type=float, help="Maximum energy for band structure", default=10.0)
    
    band_parser = subparsers.add_parser('band', help='Plot band structure')
    band_parser.add_argument('input_file', help='Input EIGENVAL file')
    band_parser.add_argument('--output', default='band.png', help='Output file name')
    band_parser.add_argument('--direction', choices=['x', 'y', 'z'], 
                            default='z', help='High symmetry direction')
    band_parser.add_argument('--below', type=float, default=5.0,
                            help='Energy range below Fermi level (eV)')
    band_parser.add_argument('--above', type=float, default=5.0,
                            help='Energy range above Fermi level (eV)')
    band_parser.add_argument('--colors', nargs='+', 
                            help='Colors for each spin channel')
    band_parser.add_argument('--show', action='store_true',
                            help='Show interactive plot')

    # pdos parser
    pdos_parser = subparsers.add_parser("pdos", help="Plot PDOS")
    pdos_parser.add_argument("input_file", type=str, help="The data file of PDOS")
    pdos_parser.add_argument("--output", type=str, help="The output file for PDOS", default="pdos.png")
    pdos_parser.add_argument("--emin", type=float, help="Minimum energy for PDOS", default=-10.0)
    pdos_parser.add_argument("--emax", type=float, help="Maximum energy for PDOS", default=10.0)
    pdos_parser.add_argument("--pdos_type", choices=["spdDOS", "totalDOS", "PDOS"], default="spdDOS", help="Type of PDOS to plot")
    pdos_parser.add_argument("--colors", nargs="+", help="Colors for PDOS plot", default=["#fdebaa", "#edc3a5", "#dbe4fb", "#abd1bc", "#e3bbed", "#cccc99", 
                                                                                          "#bed0f9", "#fcb6a5", "#f1f1f1"])
    pdos_parser.add_argument("--alpha", type=float, help="Transparency level for PDOS plot", default=0.8)

    # delta G parser
    delta_parser = subparsers.add_parser("delta_G", help="Plot delta G")
    delta_parser.add_argument("input_file", type=str, help="The data file of delta G")
    delta_parser.add_argument("--output", type=str, help="The output file for delta G", default="delta_G.png")

    args = parser.parse_args()

    if args.menu == "band":
        # plot_band_structure(args.input_file, args.output, args.emin, args.emax)
        plot_band_structure(args.input_file, args.output, args.direction, args.below, args.above, args.colors, args.show)
    elif args.menu == "pdos":
        plot_pdos(args.input_file, args.output, args.emin, args.emax, args.pdos_type, args.colors, args.alpha)
    elif args.menu == "delta_G":
        plot_delta_G(args.input_file, args.output)
