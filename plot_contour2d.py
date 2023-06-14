""" 2D contour visualization of scalar data such as potential (phisp) and electron density (nd1p).

Usage
-----
$ python plot_cmap2d.py --help

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
        description='2D contour visualization of scalar data such as potential (phisp) and electron density (nd1p).'
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

    # Visualize data on a central x-z plane as an example.
    nz, ny, nx = data3d.shape
    xs = np.arange(nx)
    zs = np.arange(nz)
    X, Z = np.meshgrid(xs, zs)
    data2d = data3d[:, ny//2, :]

    # Visualization with matplotlib.
    fig = plt.figure()
    cont = plt.contour(X, Z, data2d,
                       levels=5,
                       # colors=['black'],
                       alpha=1.0)
    cont.clabel(fmt='%1.1f', fontsize=12)

    plt.title(f'{dname}')
    plt.xlabel('x [grid]')
    plt.ylabel('z [grid]')

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'{dname}_{args.index}_contour2d.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
