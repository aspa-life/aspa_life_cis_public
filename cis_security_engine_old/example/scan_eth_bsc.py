import os
import sys
sys.path.append("../engine")
import cise

eth_list = [
        '0xc162e59cf158c0e9aa06c4c3c66a2ce2961777ee', #Black Rabbit AI
        '0x888888888888f195E27A2E0F98D712952aB9348e', #Shorter Finance
        ]

bsc_list = [
    '0x84DaD409b97082b7a6C1eA063b2Ae016C696CA9e', #All U can
    '0xe5b5d4bea7468b4994fa676949308a79497aa24c', #Sheikh Inu
]

output_files = cise.scan(eth_address=eth_list[0], bsc_address=bsc_list[0])
if output_files == None:
    print("no output was returned from cise scan")
    sys.exit(1)
else:
    print("received following output files: ")
    for f in output_files:
        print(f)
