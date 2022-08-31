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
add = contract.functions.addRealNews("Noticia de prueba", "Editor de prueba").buildTransaction({"chainId": 1337, "from": user_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
sign_add = w3.eth.account.sign_transaction(add, private_key=private_key)
send_store_contact = w3.eth.send_raw_transaction(sign_add.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

# Comprobar longitud de la lista
num = contract.functions.getNewsRecordsCount().call()
print("Numero de noticias registrados: " + str(num))

# Buscar noticia en la lista
news = contract.functions.searchNews(num).call()
print(news)

# Cambiar estado de la noticia

admin_address = "0x6fe59F29b094b4C7845267A2d130Ad584E4Db4FA"
private_key2 = "0x5b371b16a0877fd36b94186199b0a3a21babc557494d912da9120a589eee2884"

# ID de la noticia
id = news[2]

nonce = w3.eth.getTransactionCount(admin_address)
chain_id = 1337
revoke = contract.functions.changeStatusofNews(id, False).buildTransaction({"chainId": chain_id, "from": admin_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
sign_revoke = w3.eth.account.sign_transaction(revoke, private_key=private_key2)
send_store_contact = w3.eth.send_raw_transaction(sign_revoke.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)


# Comprobar estado de la noticia
news = contract.functions.searchNews(num).call()
print(news)
