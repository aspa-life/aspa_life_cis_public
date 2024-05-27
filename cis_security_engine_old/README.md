# CoInsured Security Engine (CISE), A Smart Contract Security Engine

- [CoInsured Security Engine (CISE), A Smart Contract Security Engine](#coinsured-security-engine-cise-a-smart-contract-security-engine)
  - [Description](#description)
  - [Supported file types and block chains](#supported-file-types-and-block-chains)
  - [Installation](#installation)
  - [Usage](#usage)


## Description
CISE engine can scan solidity source files and smart contracts on BSC and ETH netwoks. It performs static analysis and symbolic execution to find potential vulnerabilities and output reports in json format. 

## Supported file types and block chains
CISE currently supports:
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

