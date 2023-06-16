""" 2D vector visualization of vector data such as current (j1x, j2y) and electric field (ez).

Usage
-----
$ python plot_vector2d.py --help

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
        description='2D vector visualization of vector data such as current (j1x, j2y) and electric field (ez).'
    )

    parser.add_argument('directory',
                        default='./',
                        nargs='?',
                        help='Directory where simulation output data exists')
    parser.add_argument('--index', '-i', type=int,
                        default=-1, help='Output index')
    parser.add_argument('--output', '-o', default=None,
                        help='Output image file name')
    parser.add_argument('--dname', '-dn', default='j1',
                        help='Vector field data name')
    parser.add_argument('--axis', '-a', default='xy', choices=['xy', 'xz', 'yz'])
    parser.add_argument('--x', '-x', default=None, type=int)
    parser.add_argument('--y', '-y', default=None, type=int)
    parser.add_argument('--z', '-z', default=None, type=int)
    parser.add_argument('--rescale', '-r', default=1.0, type=float,
                        help='Multiplication factor to rescale data')

    return parser.parse_args()


def load_data3d(h5_filepath, index):
    """ Load field data from HDF5 file output by EMSES.
    """
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
    axis0 = 'zyx'.index(args.axis[0])
    axis1 = 'zyx'.index(args.axis[1])

    dname0 = f'{dname}{args.axis[0]}'
    h5_filepath = directory / f'{dname0}00_0000.h5'
    data3d0 = load_data3d(h5_filepath, args.index)

    dname1 = f'{dname}{args.axis[0]}'
    h5_filepath = directory / f'{dname1}00_0000.h5'
    data3d1 = load_data3d(h5_filepath, args.index)

    # Visualize data on a central x-z plane as an example.
    nz, ny, nx = data3d0.shape

    x = args.x or nx//2
    y = args.y or ny//2
    z = args.z or nz//2
    positions = [z, y, x]
    positions[axis0] = slice(None)
    positions[axis1] = slice(None)
    positions = tuple(positions)

    horizons = np.arange(data3d0.shape[axis0])
    verticals = np.arange(data3d0.shape[axis1])
    H, V = np.meshgrid(horizons, verticals)
    data2d0 = data3d0[positions]*args.rescale
    data2d1 = data3d1[positions]*args.rescale

    # Set grid interval to make arrows easier to see.
    nskipx = 4
    nskipz = 4
    H = H[::nskipz, ::nskipx]
    V = V[::nskipz, ::nskipx]
    data2d0 = data2d0[::nskipz, ::nskipx]
    data2d1 = data2d1[::nskipz, ::nskipx]

    # Visualization with matplotlib.
    fig = plt.figure()
    plt.quiver(H, V, data2d0, data2d1,
               angles='xy',
               scale_units='xy')

    plt.title(f'{dname}{args.axis}')
    plt.xlabel(f'{args.axis[0]} [grid]')
    plt.ylabel(f'{args.axis[1]} [grid]')

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'{dname}{args.axis}_{args.index}_{args.axis}_vector2d.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
