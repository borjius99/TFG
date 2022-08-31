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


contract = w3.eth.contract(address=contract_address, abi=abi)

nonce = w3.eth.getTransactionCount(user_address)
chain_id = 1337
contract = w3.eth.contract(address=contract_address, abi=abi)

# Añadir una organización
ejemplo = contract.functions.addOrganization(user_address, "Prueba Org", "https://www.google.com").buildTransaction({"chainId": chain_id, "from": user_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
sign_ejemplo = w3.eth.account.sign_transaction(
    ejemplo, private_key=private_key)
send_store_contact = w3.eth.send_raw_transaction(sign_ejemplo.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

# Comprobar longitud de la lista
num = contract.functions.getOrgRecordsCount().call()

print("Numero de usuarios registrados" + str(num))

# Buscar usuario en la lista
user = contract.functions.searchORG(num).call()

print(user)
