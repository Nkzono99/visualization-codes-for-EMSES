""" 1D timeseries visualization of scalar data such as potential (phisp) and electron density (nd1p).

Usage
-----
$ python plot_timeseries.py --help

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
    parser.add_argument('--dname', '-dn', default='phisp',
                        help='Field data name')
    parser.add_argument('--output', '-o', default=None,
                        help='Output image file name')

    return parser.parse_args()


def load_data4d(h5_filepath, indexes=None):
    if not h5_filepath.exists():
        msg = f'Error: the following h5 filepath is not found: {h5_filepath.resolve()}'
        sys.exit(msg)

    # Open HDF5 file.
    h5 = h5py.File(str(h5_filepath), 'r')

    # Obtain data at the time to be visualized.
    group = h5[list(h5.keys())[0]]
    keys = list(group.keys())
    if indexes is not None:
        keys = [keys[index] for index in indexes]
    data4d = [group[key] for key in keys]

    return np.array(data4d)


def main():
    args = parse_args()

    directory = Path(args.directory)
    dname = args.dname

    h5_filepath = directory / f'{dname}00_0000.h5'

    data4d = load_data4d(h5_filepath)

    # Visualize timeseries data on a center point as an example.
    nt, nz, ny, nx = data4d.shape
    ts = np.arange(nt)
    data1d = data4d[:, nz//2, ny//2, nx//2]

    # Visualization with matplotlib.
    fig = plt.figure()
    plt.plot(ts, data1d)

    plt.title(f'{dname}')
    plt.xlabel('t [step / output interval]')
    plt.ylabel(f'{dname}')
    plt.grid()

    # Save plotted image to <directory>/data/***.png.
    directory_to_save = directory / 'data'
    directory_to_save.mkdir(exist_ok=True)

    if args.output:
        output_filename = args.output
    else:
        output_filename = f'{dname}_timeseries.png'

    fig.tight_layout()
    fig.savefig(directory_to_save / output_filename)


if __name__ == '__main__':
    main()
