from web3 import Web3
import json
from solcx import compile_standard, install_solc


private_key = '0x59f4ec89a1de1f4d5000fd5ad95a9e09b9eb8e8d8d43732e342c61284eb77932'
user_address = '0x588562BC7890667Ba0766CF7805a30541F7199FD'
contract_address = '0x6C1C91FD998E4C5CDba63c628d80f2563348b6c1'


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))


with open("FakeNews/compiled_code.json", "r") as file:
    compiled_sol = file.read()

compiledJson = json.loads(compiled_sol)

# get abi
abi = json.loads(compiledJson["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]


# Añadir una noticia
nonce = w3.eth.getTransactionCount(user_address)
contract = w3.eth.contract(address=contract_address, abi=abi)

array = contract.functions.returnORGarraywithNews(0).call()

print(array)
print(len(array))
