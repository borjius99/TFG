from web3 import Web3
import json
from solcx import compile_standard, install_solc
from Crypto.PublicKey import RSA
import pandas as pd
from pandas import json_normalize


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
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)
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
    with open("compiled_code.json", "r") as file:
        compiled_sol = file.read()

    compiledJson = json.loads(compiled_sol)

    # get abi
    abi = json.loads(compiledJson["contracts"]["contract.sol"]["fightFakeNews"]["metadata"])["output"]["abi"]
    return abi


def addOrganization(contract_address, abi, admin_address, private_key, user_address, org_name, org_source):
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        try:
            nonce = w3.eth.getTransactionCount(admin_address)
            chain_id = 1337
            contract = w3.eth.contract(address=contract_address, abi=abi)
            print('aqui')
            ejemplo = contract.functions.addOrganization(user_address, org_name, org_source).buildTransaction({"chainId": chain_id, "from": admin_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
            sign_ejemplo = w3.eth.account.sign_transaction(
                ejemplo, private_key=private_key)
            send_store_contact = w3.eth.send_raw_transaction(sign_ejemplo.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)
            return True
        except Exception as e:
            return False
    else:
        return False


def addNews(contract_address, abi, wallet, newsTitle, publisher, private_key):
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        try:
            nonce = w3.eth.getTransactionCount(wallet)
            contract = w3.eth.contract(address=contract_address, abi=abi)
            add = contract.functions.addRealNews(newsTitle, publisher).buildTransaction({"chainId": 1337, "from": wallet, "gasPrice": w3.eth.gas_price, "nonce": nonce})
            sign_add = w3.eth.account.sign_transaction(add, private_key=private_key)
            send_store_contact = w3.eth.send_raw_transaction(sign_add.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)
            return True
        except Exception as e:
            return False
    else:
        return False


def searchUsers(contract_address, abi):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numUsers = contract.functions.getOrgRecordsCount().call()
    lista = []
    for i in range(0, numUsers):
        lista.append(contract.functions.searchORG(i).call())

    df = pd.DataFrame(lista, columns=['Address', 'ID', 'Nombre', 'Web', 'Puede publicar'])
    return df, numUsers


def searchUserByWallet(contract_address, abi, wallet):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numOrg = contract.functions.getOrgRecordsCount().call()

    for i in range(0, numOrg):
        address = contract.functions.searchORG(i).call()
        if (address[0] == wallet):
            return address[1]
    return -1


def searchNews_byName(contract_address, abi, title):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numNews = contract.functions.getNewsRecordsCount().call()
    for i in range(100000, 100000+numNews):
        news = contract.functions.searchNews(i).call()
        if news[3] == title:
            return news, True


def searchOrg_byAddress(contract_address, abi, address):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numOrgs = contract.functions.getOrgRecordsCount().call()
    print(numOrgs)
    for i in range(numOrgs):
        orgs = contract.functions.searchORG(i).call()
        print(orgs)
        if orgs[0] == address:
            return orgs


def revokeStatus(contract_address, admin_address, abi, wallet, private_key):
    w3 = connectToBlockchain()

    id = searchUserByWallet(contract_address, abi, wallet)
    if id >= 0:
        contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(admin_address)
        chain_id = 1337
        revoke = contract.functions.changeStatusofORGs(id, False).buildTransaction({"chainId": chain_id, "from": admin_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
        sign_revoke = w3.eth.account.sign_transaction(revoke, private_key=private_key)
        send_store_contact = w3.eth.send_raw_transaction(sign_revoke.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)
        return True
    else:
        return False


def revokeNewsStatus(contract_address, admin_address, abi, id, private_key):
    w3 = connectToBlockchain()

    contract = w3.eth.contract(address=contract_address, abi=abi)
    nonce = w3.eth.getTransactionCount(admin_address)
    chain_id = 1337
    revoke = contract.functions.changeStatusofNews(id, False).buildTransaction({"chainId": chain_id, "from": admin_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
    sign_revoke = w3.eth.account.sign_transaction(revoke, private_key=private_key)
    send_store_contact = w3.eth.send_raw_transaction(sign_revoke.rawTransaction)
    transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_contact)

    return True


def showNews(contract_address, abi):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numNews = contract.functions.getNewsRecordsCount().call()
    lista = []
    for i in range(0, numNews):
        lista.append(contract.functions.searchNews(100000+i).call())
    df = pd.DataFrame(lista, columns=['ID Organización', 'Nombre Organización', 'ID Noticia', 'Titulo', 'Editor', 'Veracidad'])

    return df


def searchNews(contract_address, abi, id):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    news = contract.functions.searchNews(id).call()
    return news


def hasVoted(id, voters):
    y = json.loads(voters)
    numVoters = len(y["voters"])
    for i in range(numVoters):
        if y["voters"][i] == id:
            return True
    return False


def searchOrgNews(contract_address, abi, orgID):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    array = contract.functions.returnORGarraywithNews(orgID).call()
    lista = []
    for i in array:
        lista.append(contract.functions.searchNews(i).call())
    df = pd.DataFrame(lista, columns=['ID Organización', 'Nombre Organización', 'ID Noticia', 'Titulo', 'Editor', 'Veracidad'])

    return df
