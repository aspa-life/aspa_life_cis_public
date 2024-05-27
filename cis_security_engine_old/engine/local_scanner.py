import os
import sys
import time
import subprocess
import argparse
import json
from timeit import default_timer as timer

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--directory", help="a folder of solidity files to scan")

def displayJsonReport(fid_json):
    json_data = json.load(fid_json)
    issue_keys = ["swcTitle",
                  "severity",
                  "swcID",
                  "description",
                  "locations"]
    for each_data in json_data:
        print("sourceList: ", each_data["sourceList"])
        print("sourceFormat: ", each_data["sourceFormat"])     
        print("found %d issues"%(len(each_data["issues"])))
        for issue in each_data["issues"]:
            print("\n********************")
            for k in issue_keys:
                if k == "description":
                    print(k,":")
                    print("\t%s"%(issue[k]["head"]))
                    print("\t%s"%(issue[k]["tail"]))
                else:
                    print("%s: %s"%(k, issue[k]))

def get_solc_version(solfile):
    with open(solfile, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            # check if string present on a current line
            if line.find(r'pragma solidity ^') != -1:
               return line[line.find(r'^')+1:line.find(r';')]
    return None 

def static_analysis(solfile):
    '''perform static analysis on a single sol file'''

    # choose solc version
    solc_ver = get_solc_version(solfile)
    if solc_ver:
        subprocess.run(["solc-select", "use", solc_ver])

    # set json file and run
    outjson = solfile.replace(".sol","_static.json")
    sacmd = ["slither", solfile,"--json", outjson]
    print("\nStatic analysis on %s, output %s"%(solfile, outjson))
    st = timer()
    outSA = subprocess.Popen(sacmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while outSA.poll() == None:
        print("Static analysis is still in progress, time elapsed %d seconds"%(timer()-st))
        time.sleep(5)

    [out, err] = outSA.communicate()
    et = timer()
    print("Static analysis on %s finished in %d seconds" %(solfile, et-st))
    return outjson

def scan_files(files=None):
    '''scan a list of .sol files'''
    out_file_list = []
    for solfile in files:
        if not solfile.endswith('.sol'):
            continue

        # static
        out_file_list.append(static_analysis(solfile))

        # symbolic
        mythcmd = ["myth","-v", "4", "analyze", solfile, "-t","3","-o","jsonv2",'--execution-timeout','400']
        #mythcmd = ["myth","-v", "4", "analyze", solfile, "-o","jsonv2"]

        # print(mythcmd)

        report = solfile.replace(".sol", '_Sym.json')
        with open(report, 'w') as fid_report:
            print("\nscanning %s, output %s"%(solfile, report))
            st = timer()
            outMyth = subprocess.Popen(mythcmd, stdout=fid_report, stderr=subprocess.PIPE)

            while outMyth.poll() == None:
                print("scanning is still in progress, time elapsed %d seconds"%(timer()-st))
                time.sleep(5)

            [out, err] = outMyth.communicate()
            et = timer()
            print("scanning %s finished in %d seconds" %(solfile, et-st))
            # print(out.decode())
            # print(err.decode())
        # with open(report, 'r') as fid_json:
        #     displayJsonReport(fid_json)
        out_file_list.append(report)
    
    return out_file_list


def scan_dir(directory="."):
    '''Scan all .sol files in a directory'''
    if not directory.startswith("/"):
        dirFullPath = os.path.join(os.getcwd(), directory)
    else:
        dirFullPath = directory
    fileList = []
    fileList += [os.path.join(dirFullPath, f) for f in os.listdir(dirFullPath) \
        if os.path.isfile(os.path.join(dirFullPath,f)) and f.endswith(".sol")]

    return scan_files(fileList)


if __name__ == "__main__":
    try:
        args = parser.parse_args()
        scan_dir(args.directory)
    except:
        sys.exit(1)
