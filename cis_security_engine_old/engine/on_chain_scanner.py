import os
import sys
import json
import subprocess
from timeit import default_timer as timer
import time

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

def static_analysis(ethaddress):
    
    outjson = "reports/" + ethaddress.replace(':','_') + "_SA.json"
    sacmd = ["slither", ethaddress,"--json", outjson]
    print("\nStatic analysis on %s, output %s"%(ethaddress, outjson))
    
    st = timer()
    outSA = subprocess.Popen(sacmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while outSA.poll() == None:
        print("Static analysis is still in progress, time elapsed %d seconds"%(timer()-st))
        time.sleep(5)

    [out, err] = outSA.communicate()
    et = timer()
    print("Static analysis on %s finished in %d seconds" %(ethaddress, et-st))
    return outjson


def auditContractByAddress(eth_addr=None, bsc_addr=None):
    
    out_file_list = []
    for i, addr in enumerate([eth_addr, bsc_addr]):
        if addr == None:
            continue
          
        outjson = 'reports/'+addr+'_Sym.json'
        with open(outjson, 'w') as fid_outjson:
            mythcmd = ["myth", "-v4", "analyze", "-a", addr, "-o", "jsonv2", 
                        "--infura-id", "7188fbb9e7aa48d2af85b49c976ab04b",
                        "--execution-timeout", "300"]
            if i == 1:
                mythcmd += ["--rpc","bsc-dataseed1.binance.org:443","--rpctls","True"]
            print("scanning %s, output %s"%(addr, outjson))
            st = timer()
            outMyth = subprocess.Popen(mythcmd, stdout=fid_outjson, stderr=subprocess.PIPE)

            while outMyth.poll() == None:
                print("scanning is still in progress, time elapsed %d seconds"%(timer()-st))
                time.sleep(5)

            [out, err] = outMyth.communicate()
            et = timer()
            print("scanning %s finished in %d seconds" %(addr, et-st))
            # print(out)
            # print(err)
        # with open(report,'r') as fid_json:
        #     displayJsonReport(fid_json)
        out_file_list.append(outjson)

    return out_file_list

def auditAllContractFound():
    with open('ContractList.txt', 'r') as f:
        for line in f:
            print('Auditing ' + line.rstrip('\n') + ' contract \n...')
            auditContractByAddress(line.rstrip('\n'))

def scan(eth_addr=None, bsc_addr=None):

    out_file_list = []
    if eth_addr:
        out_file_list.append(static_analysis(eth_addr))

    if bsc_addr:
        out_file_list.append(static_analysis('bsc:'+bsc_addr))

    print("\nscanning on-chain smart contract %s"%(eth_addr))
    out_file_list += auditContractByAddress(eth_addr, bsc_addr)
    
    return out_file_list

if __name__ == "__main__":
    try:
        # sys.exit(main('0xEbFD99838cb0c132016B9E117563CB41f2B02264'))
        scan('0xbe247600c83b8aE51E8c72960cC2D2f128D50dD3')
    except:
        sys.exit(-1)
