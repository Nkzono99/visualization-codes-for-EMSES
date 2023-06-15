# Using python3.8.8.
if [ ! -e ./get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
fi

# Install libraries
pip install -r requirements.txt
python configuration-test/test-matplotlib.py # Test if the libraries are installed


# Install mpi4py
wget https://github.com/mpi4py/mpi4py/releases/download/3.1.4/mpi4py-3.1.4.tar.gz
tar xf mpi4py-3.1.4.tar.gz
cd mpi4py-3.1.4/

echo "[mpt]" >> mpi.cfg
echo "mpi_dir              = /opt/hpe/hpc/mpt/mpt-2.23" >> mpi.cfg
echo "mpicc                = %(mpi_dir)s/bin/mpicc" >> mpi.cfg
echo "mpicxx               = %(mpi_dir)s/bin/mpicxx" >> mpi.cfg
echo "include_dirs         = %(mpi_dir)s/include" >> mpi.cfg
echo "libraries            = mpt" >> mpi.cfg
echo "library_dirs         = %(mpi_dir)s/lib" >> mpi.cfg

python setup.py build --mpi=mpt
python setup.py install --user

# Test if mpi4py is installed
cd ../
mpiexec -n 4 python configuration-test/test-mpi4py.py
mpiexec -n 4 python -m mpi4py.futures configuration-test/test-mpi4py-futures.py
