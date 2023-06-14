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

    h5_filepath = directory / f'j1x00_0000.h5'
    j1x3d = load_data3d(h5_filepath, args.index)

    h5_filepath = directory / f'j1z00_0000.h5'
    j1z3d = load_data3d(h5_filepath, args.index)

    # Visualize data on a central x-z plane as an example.
    nz, ny, nx = j1x3d.shape
    xs = np.arange(nx)
    zs = np.arange(nz)
    X, Z = np.meshgrid(xs, zs)
    j1x2d = j1x3d[:, ny//2, :]
    j1z2d = j1z3d[:, ny//2, :]

    # Set grid interval to make arrows easier to see.
    nskipx = 4
    nskipz = 4
    X = X[::nskipz, ::nskipx]
    Z = Z[::nskipz, ::nskipx]
    j1x2d = j1x2d[::nskipz, ::nskipx]
    j1z2d = j1z2d[::nskipz, ::nskipx]

    # Visualization with matplotlib.
    fig = plt.figure()
    plt.quiver(X, Z, j1x2d, j1z2d,
               angles='xy',
               scale_units='xy')

    plt.title(f'j1xz')
    plt.xlabel('x [grid]')
    plt.ylabel('z [grid]')

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'j1xz_{args.index}.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
