from web3 import Web3
import json
from solcx import compile_standard, install_solc

private_key = '0x5b371b16a0877fd36b94186199b0a3a21babc557494d912da9120a589eee2884'
admin_address = '0x6fe59F29b094b4C7845267A2d130Ad584E4Db4FA'


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

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
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.4.20",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["contract.sol"]["fightFakeNews"]["evm"]["bytecode"]["object"]

abi = json.loads(compiled_sol["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]

address = admin_address
chain_id = 1337
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(address)

transaction = contract.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": address,
        "nonce": nonce,
    }
)
sign_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
transaction_hash = w3.eth.send_raw_transaction(sign_transaction.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

contract_address = transaction_receipt.contractAddress

print(contract_address)
