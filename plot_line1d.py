""" 1D visualization of field data such as potential (phisp) and electron density (nd1p).

Usage
-----
$ python plot_line1d.py --help

"""
import sys
from argparse import ArgumentParser
from pathlib import Path

import h5py
import matplotlib.pyplot as plt
import numpy as np


def parse_args():
    """ Parses command line arguments. 

        See official document (https://docs.python.org/3/library/argparse.html).
    """
    parser = ArgumentParser(
        description='1D visualization of field data such as potential (phisp) and electron density (nd1p).'
    )

    parser.add_argument('directory',
                        default='/home/t23545/work/flat_hole_comp/exp_hole_with_bluk_3',
                        nargs='?',
                        help='Directory where simulation output data exists')
    parser.add_argument('--index', '-i', type=int,
                        default=-1, help='Output index')
    parser.add_argument('--dname', '-dn', default='phisp',
                        help='Field data name')
    parser.add_argument('--output', '-o', default=None,
                        help='Output image file name')

    return parser.parse_args()


def load_data3d(h5_filepath, index):
    if not h5_filepath.exists():
        msg = f'Error: the following h5 filepath is not found: {h5_filepath.resolve()}'
        sys.exit(msg)

    # Open HDF5 file.
    h5 = h5py.File(str(h5_filepath), 'r')

    # Obtain data at the time to be visualized.
    group = h5[list(h5.keys())[0]]
    data3d = group[list(group.keys())[index]]

    return data3d


def main():
    args = parse_args()

    directory = Path(args.directory)
    dname = args.dname

    h5_filepath = directory / f'{dname}00_0000.h5'

    data3d = load_data3d(h5_filepath, args.index)

    # Visualize data on a central axis parallel to the z-axis as an example.
    nz, ny, nx = data3d.shape
    zs = np.arange(nz)
    data1d = data3d[:, ny//2, nx//2]

    # Visualization with matplotlib.
    fig = plt.figure()
    plt.plot(zs, data1d)

    plt.title(f'{dname}')
    plt.xlabel('z [grid]')
    plt.ylabel(f'{dname}')
    plt.grid()

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'{dname}_{args.index}_line1d.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
