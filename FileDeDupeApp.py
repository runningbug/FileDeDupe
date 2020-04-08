# FileDeDupe v1.0
# @Gamemaker_uk
# 24/04/2018
#
# DISCLAIMER:
#
# This SOFTWARE PRODUCT is provided by THE PROVIDER "as is" and "with all faults." 
# THE PROVIDER makes no representations or warranties of any kind concerning the safety, 
# suitability, lack of viruses, inaccuracies, typographical errors, or other harmful 
# components of this SOFTWARE PRODUCT. There are inherent dangers in the use of any 
# software, and you are solely responsible for determining whether this SOFTWARE PRODUCT 
# is compatible with your equipment and other software installed on your equipment. 
# You are also solely responsible for the protection of your equipment and backup of your data, 
# and THE PROVIDER will not be liable for any damages you may suffer in connection with using,
# modifying, or distributing this SOFTWARE PRODUCT. 
#
# LICENSE: DO WHATEVER YOU LIKE WITH IT

import os
import sys
import argparse
from FileDeDupe import FileDeDupe

try:

    pro = "FileDeDupe DELETES FILES FROM YOU FILE SYSTEM. ONLY USE ON A _COPY_ OF YOUR DATA. YOU USE THIS PROGRAM AT YOUR OWN RISK!"

    ep =  "FileDeDupe searches the file system and finds which files are identical. "
    ep += "It then determines which file out of the set is the original and deletes all duplicates. "
    ep += "Example: \"python3 FileDeDupeApp.py d:\\photos\". "
    ep += "If you don't want to be asked which file in a set of duplicate to keep, specify the -autodelete option. "
    ep += "Example: \"python3 FileDeDupeApp.py d:\\photos -autodelete\". "
    ep += "If you want to supress non-essential output, specify the -quiet option. "
    ep += "Example: \"python3 FileDeDupeApp.py d:\\photos -quiet\"."

    if (sys.version_info < (3,6)):
        raise ValueError("FileDeDupe Requires Python Version 3.6 or greater.")
    
    parser = argparse.ArgumentParser(description=pro, epilog=ep)  
    parser.add_argument('path', help='Mandatory argument that sets the path to be recursivley traversed')
    parser.add_argument("--autodelete", help="FileDeDupe will automatically delete all duplicates without asking the user.", action="store_true")
    parser.add_argument("--version", action='version', version="FileDeDupe v1.0") 
    parser.add_argument("--quiet", help="Do not show verbose output", action="store_true")
    args = parser.parse_args()

    fileDeDupeApp = FileDeDupe(args.path, (not (args.quiet)))
    fileDeDupeApp.DeleteAllDuplicates((not (args.autodelete)), (not (args.quiet)))

except ValueError as e:
    print("Error: ", e)