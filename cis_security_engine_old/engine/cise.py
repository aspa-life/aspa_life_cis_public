import os
import sys

import local_scanner as lsn
import on_chain_scanner as ocsn

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s","--sol", help="solidity source file to scan")
parser.add_argument("-d","--directory", help="scan all solidity source files in a directory")
parser.add_argument("-b","--bsc", help="scan smart contract on bsc network")
parser.add_argument("-e","--eth", help="scan smart contract on eth network")

def scan(dir=None, files=None, bsc_address=None, eth_address=None):
    
    out_file_list = []
    try:
        # create reports folder for output files
        reports_dir = os.path.join(os.getcwd(),'reports')
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)

        # scan a folder
        if dir:
            out_file_list += lsn.scan_dir(dir)

        # scan a file list
        if files:
            out_file_list += lsn.scan_files(files)

        # scan smart contracts on eth and/or bsc
        out_file_list += ocsn.scan(bsc_addr=bsc_address, eth_addr=eth_address)

    except OSError as err:
        print("exception: {}".format(err))
    
    else:
        print("cise scan() finished!")

    finally:
        return out_file_list





if __name__ == "__main__":
    args = parser.parse_args()
    sys.exit(scan(dir=args.directory, files=args.sol, bsc_address=args.bsc, eth_address=args.etch))
