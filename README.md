usage: FileDeDupeApp.py [-h] [--autodelete] [--version] [--quiet] path

FileDeDupe DELETES FILES FROM YOUR FILE SYSTEM. ONLY USE ON A _COPY_ OF YOUR DATA. YOU USE THIS PROGRAM AT YOUR OWN
RISK!

positional arguments:
  path          Mandatory argument that sets the path to be recursivley traversed

optional arguments:
  -h, --help    show this help message and exit
  --autodelete  FileDeDupe will automatically delete all duplicates without asking the user to select which file to delete.
  --version     show program's version number and exit
  --quiet       Do not show verbose output

FileDeDupe searches the file system and finds which files are identical. It then determines which file out of the set
is the original and deletes all duplicates. 

Example: "python3 FileDeDupeApp.py d:\photos". 

If you don't want to be asked which file in a set of duplicate to keep, specify the -autodelete option.

Example: "python3 FileDeDupeApp.py d:\photos -autodelete". 

If you want to supress non-essential output, specify the -quiet option. 

Example: "python3 FileDeDupeApp.py d:\photos -quiet".