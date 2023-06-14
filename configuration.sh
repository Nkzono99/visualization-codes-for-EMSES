# Using python3.8.8.
if [ ! -e ./get-pip.py ]; then
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
fi

pip install -r requirements.txt

