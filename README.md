# pyHash
## Description
pyHash is supposed to be an easy solution for calculating a SHA256 hash.
It's able to calculate hashes for a single file and a whole directory. Furthermore it can compare hashes a file and all files of two directories.
This can be especially useful when comparing backups.
## Getting started
To be able to use this python script you need the following:
- [Python 3](https://www.python.org/downloads/)
- Install the [requirements.txt](requirements.txt) (`install -r requirements.txt`)
## Usage example
- Calculate a hash of a single file:<br>
`py .\pyHash.py sha256 c:\\pyHash\\pyHash.py`
- Calculate hashes of all files in a directory:<br>
`py .\pyHash.py dir_hash c:\\pyHash`
- Compare two files:<br>
`py .\pyHash.py compare_files c:\\pyHash_old\\pyHash.py  c:\\pyHash_new\\pyHash.py`
- Compare two directories:<br>
`py .\pyHash.py compare_dir c:\\pyHash_old c:\\pyHash_new`
#   p y H a s h  
 