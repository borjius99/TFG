import json
from web3 import Web3
from solcx import compile_standard, install_solc
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
print(w3.isConnected())

address = '0x8E035E241956D0C2aa01decb75d7b53670A53C60'
private_key = '0xc9e41a2a429b1fac3e38386e872ba08151c1269cbf3baaacf98daaba272ccb50'
chain_id = 1337
nonce = w3.eth.getTransactionCount(address)

print(nonce)

with open("compiled_code.json", "r") as file:
    compiled_sol = file.read()

compiledJson = json.loads(compiled_sol)

# get abi
abi = json.loads(compiledJson["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]

contract_1 = w3.eth.contract(address='0x7ada6278A987a0aAF8471852c24C010B5791Eb96', abi=abi)

print(w3.eth.gas_price)


# Prueba Añadir Editor
'''
ejemplo = contract_1.functions.addOrganization('0x97d3B6ACD85a773Ccd6357EF728Bb9c73FA568F5', 'Marca', 'marca.com').buildTransaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
sign_ejemplo = w3.eth.account.sign_transaction(
    ejemplo, private_key='/mnt/c/Users/borji/Escritorio/TFG/FakeNews/private_borjius@gmail.com.pem')

send_store_contact = w3.eth.send_raw_transaction(sign_ejemplo.rawTransaction)

transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

print(transaction_receipt)

#Prueba añadir noticia

ejemplo = contract_1.functions.addRealNews('Primera victoria en la junquera', 'Faro de Vigo').buildTransaction({"chainId": chain_id, "from": '0x4b7466157fa97C5B182DA0436f8C1879A7cc8139', "gasPrice": w3.eth.gas_price, "nonce": nonce})

sign_ejemplo = w3.eth.account.sign_transaction(ejemplo, private_key='0x955fcfa7dc70fde58cab356f7cf0ab197b6de5d0ada0a4701945af595ee42eb0')

send_store_contact = w3.eth.send_raw_transaction(sign_ejemplo.rawTransaction)

transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

print(transaction_receipt)

ejemplo1 = contract_1.functions.getOrgRecordsCount().call()  # buildTransaction({"chainId": chain_id, "from": address, "gasPrice": w3.eth.gas_price, "nonce": nonce})

print(ejemplo1)

# Prueba Revoke Status

address2 = '0xA1A6117d24435a624e3aAAa54E95636bC4c09B85'
nonce2 = w3.eth.getTransactionCount(address2)

for i in range(0, ejemplo1):
    address = contract_1.functions.searchORG(i).call()
    print(address)
    if (address[0] == '0xc97523b69931f70ED17E7afdBF2bA5Ba4ca900f6'):
        revoke = contract_1.functions.changeStatusofORGs(address[1], False).buildTransaction({"chainId": chain_id, "from": address2, "gasPrice": w3.eth.gas_price, "nonce": nonce2})
        sign_ejemplo = w3.eth.account.sign_transaction(revoke, private_key='0x1238858eec7c417936b4875d100609bea960f3bcd9ad85785ebfa3f6f4f65124')
        send_store_contact = w3.eth.send_raw_transaction(sign_ejemplo.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)
        print(transaction_receipt)
    print('De aqui no pasa')
    añadir = contract_1.functions.addRealNews('Primera victoria', 'Faro de Vigo').buildTransaction({"chainId": chain_id, "from": address[0], "gasPrice": w3.eth.gas_price, "nonce": nonce})
    sign_ejemplo2 = w3.eth.account.sign_transaction(añadir, private_key='0x919ba8363816c46f1b1908caf11de39d2529c608fd52af4aa1893050f20321da')
    send_store_contact2 = w3.eth.send_raw_transaction(sign_ejemplo2.rawTransaction)
    transaction_receipt2 = w3.eth.wait_for_transaction_receipt(send_store_contact2)

    print(transaction_receipt2)
'''

numNews = contract_1.functions.getNewsRecordsCount().call()
for i in range(0, numNews):
    news = contract_1.functions.searchNews(i).call()
    print(news)
    if news[3] == 'Hola':
        print(news)
