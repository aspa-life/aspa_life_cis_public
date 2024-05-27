import os
import sys
sys.path.append("../engine")
import cise

dir_2scan = "sol_example"
files_2scan = ["tokensale.sol","game.sol"]
output_files = cise.scan(dir=dir_2scan)
if output_files == None:
    print("no output was returned from cise scan")
    sys.exit(1)
else:
    print("received following output files: ")
    for f in output_files:
        print(f)
