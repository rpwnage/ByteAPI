# Byte.py
Inofficial Python API Wrapper for the Byte.co app written in python.

## Installation
You can use the setup.py file to install from the github source using `python setup.py install` or just run `pip install Byte.py` to install from pypi.

## Basic usage
You can try the following example python code, to creat a new ByteAPI Client instance and print out its username.
```python
from ByteAPI import ByteAPI

byteClient = ByteAPI(<Your Token>)
print(byteClient.username)
```
