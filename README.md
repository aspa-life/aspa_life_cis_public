Note: Only small portion of code is visible to the public. To access a more complete version, please contact us at [admin@aspa.life](admin@aspa.life) .

# aspa Security Engine (ASE), A Smart Contract Security Engine

- [aspa Security Engine (ASE), A Smart Contract Security Engine](#aspa-security-engine-ase-a-smart-contract-security-engine)
  - [Description](#description)
  - [Supported file types and block chains](#supported-file-types-and-block-chains)
  - [Installation](#installation)
  - [Usage](#usage)


## Description
ASE engine can scan solidity source files and smart contracts on BSC and ETH netwoks. It performs static analysis and symbolic execution to find potential vulnerabilities and output reports in json format. 

## Supported file types and block chains
ASE currently supports:
- solidity

Block Chains supported:
- ETH
- BSC

## Installation
Install pipenv
```bash
python3 -m pip install pipenv
```
Activate pipenv shell
```bash
pipenv shell
```
Install from pipfile.loc
```bash
pipenv install --ignore-pipfile
```
Install a range of solc verions
```bash
solc-select install $(grep "0." solc.versions)
```

## Usage
Activate pipenv shell first
```bash
pipenv shell
```
You can then follow the python files in example folder to see how to use cise.py to scan:
- all .sol files in a folder
- a list of .sol files
- a smart contract address at ETH network
- a smart contract address at BSC network
```bash
cd example
python3 scan_sol.py
python3 scan_eth_bsc.py
```

You can create a pdf file from a .json scan:
```
cd example
python json_to_pdf.py
```
and follow the script steps.
