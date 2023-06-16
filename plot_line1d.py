""" 1D visualization of scalar data such as potential (phisp) and electron density (nd1p).

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
                        default='./',
                        nargs='?',
                        help='Directory where simulation output data exists')
    parser.add_argument('--index', '-i', type=int,
                        default=-1, help='Output index')
    parser.add_argument('--dname', '-dn', default='phisp',
                        help='Field data name')
    parser.add_argument('--output', '-o', default=None,
                        help='Output image file name')
    parser.add_argument('--axis', '-a', default='x', choices=['x', 'y', 'z'])
    parser.add_argument('--x', '-x', default=None, type=int)
    parser.add_argument('--y', '-y', default=None, type=int)
    parser.add_argument('--z', '-z', default=None, type=int)
    parser.add_argument('--rescale', '-r', default=1.0, type=float,
                        help='Multiplication factor to rescale data')

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
    axis = 'zyx'.index(args.axis)

    h5_filepath = directory / f'{dname}00_0000.h5'

    data3d = load_data3d(h5_filepath, args.index)

    # Visualize data on a central axis parallel to the z-axis as an example.
    nz, ny, nx = data3d.shape

    x = args.x or nx//2
    y = args.y or ny//2
    z = args.z or nz//2
    positions = [z, y, x]
    positions[axis] = slice(None)
    positions = tuple(positions)

    horizons = np.arange(data3d.shape[axis])
    data1d = data3d[positions]*args.rescale

    # Visualization with matplotlib.
    fig = plt.figure()
    plt.plot(horizons, data1d)

    plt.title(f'{dname}')
    plt.xlabel(f'{args.axis} [grid]')
    plt.ylabel(f'{dname}')
    plt.grid()

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'{dname}_{args.index}_{args.axis}_line1d.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
