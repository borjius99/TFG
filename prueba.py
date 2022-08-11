from web3 import Web3
import json
from solcx import compile_standard, install_solc
from Crypto.PublicKey import RSA
import pandas as pd
from pandas import json_normalize


private_key = '0x5b371b16a0877fd36b94186199b0a3a21babc557494d912da9120a589eee2884'
admin_address = '0x6fe59F29b094b4C7845267A2d130Ad584E4Db4FA'
contract_address = '0x6C1C91FD998E4C5CDba63c628d80f2563348b6c1'


def connectToBlockchain():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    return w3


def pushContract(private_key, a1):
    w3 = connectToBlockchain()
    with open("/mnt/c/Users/borji/Escritorio/TFG/FakeNews/FakeApp/contract.sol", "r") as file:
        fakenews_file = file.read()

    install_solc("0.4.20")

    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {"contract.sol": {"content": fakenews_file}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]  # output needed to interact with and deploy contract
                    }
                }
            },
        },
        solc_version="0.4.20",
    )

    with open("compiled_code.json", "w") as file:
        json.dump(compiled_sol, file)

    # get bytecode
    bytecode = compiled_sol["contracts"]["contract.sol"]["fightFakeNews"]["evm"]["bytecode"]["object"]

    # get abi
    abi = json.loads(compiled_sol["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]

    address = a1
    chain_id = 1337
    contract1 = w3.eth.contract(abi=abi, bytecode=bytecode)

    contract = contract1(address='0x000000000000000000000000000000000000dEaD')
    # Get the number of latest transaction
    nonce = w3.eth.getTransactionCount(address)

    # build transaction
    transaction = contract.constructor().buildTransaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    # Sign the transaction
    sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Deploying Contract!")
    # Send the transaction
    transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
    # Wait for the transaction to be mined, and get the transaction receipt
    print("Waiting for transaction to finish...")
    transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    print(f"Done! Contract deployed to {transaction_receipt.contractAddress}")

    contract_address = transaction_receipt.contractAddress

    return contract_address, abi


def getAbi():
    with open("FakeNews/compiled_code.json", "r") as file:
        compiled_sol = file.read()

    compiledJson = json.loads(compiled_sol)

    # get abi
    abi = json.loads(compiledJson["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]
    return abi


abi = getAbi()

w3 = connectToBlockchain()
contract = w3.eth.contract(address=contract_address, abi=abi)
numUsers = contract.functions.returnORGarraywithNews(0).call()
print(numUsers)
lista = []
for i in numUsers:
    lista.append(contract.functions.searchNews(i).call())

print(lista)
