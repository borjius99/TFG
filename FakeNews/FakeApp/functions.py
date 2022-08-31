from web3 import Web3
import json
from solcx import compile_standard, install_solc
import pandas as pd
from pandas import json_normalize


def connectToBlockchain():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    return w3


def getAbi():
    with open("compiled_code.json", "r") as file:
        compiled_sol = file.read()

    compiledJson = json.loads(compiled_sol)

    abi = json.loads(compiledJson["contracts"]["contract.sol"]
                     ["fightFakeNews"]["metadata"])["output"]["abi"]
    return abi


def addOrganization(contract_address, abi, private, user_address, org_name, org_source):
    w3 = connectToBlockchain()
    if w3.isConnected() is True:
        try:
            nonce = w3.eth.getTransactionCount(user_address)
            chain_id = 1337
            contract = w3.eth.contract(address=contract_address, abi=abi)
            ejemplo = contract.functions.addOrganization(user_address, org_name, org_source).buildTransaction(
                {"chainId": chain_id, "from": user_address, "gasPrice": w3.eth.gas_price, "nonce": nonce})
            sign_ejemplo = w3.eth.account.sign_transaction(
                ejemplo, private_key=private)
            send_store_contact = w3.eth.send_raw_transaction(
                sign_ejemplo.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(
                send_store_contact)
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
            add = contract.functions.addRealNews(newsTitle, publisher).buildTransaction(
                {"chainId": 1337, "from": wallet, "gasPrice": w3.eth.gas_price, "nonce": nonce})
            sign_add = w3.eth.account.sign_transaction(
                add, private_key=private_key)
            send_store_contact = w3.eth.send_raw_transaction(
                sign_add.rawTransaction)
            transaction_receipt = w3.eth.wait_for_transaction_receipt(
                send_store_contact)
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

    df = pd.DataFrame(
        lista, columns=['Address', 'ID', 'Nombre', 'Web', 'Puede publicar'])
    return df, numUsers


def searchNews_byName(contract_address, abi, title):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numNews = contract.functions.getNewsRecordsCount().call()
    for i in range(100000, 100000 + numNews):
        news = contract.functions.searchNews(i).call()
        if news[3] == title:
            return news


def searchOrg_byAddress(contract_address, abi, address):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numOrgs = contract.functions.getOrgRecordsCount().call()
    for i in range(numOrgs):
        orgs = contract.functions.searchORG(i).call()
        if orgs[0] == address:
            return orgs


def revokeStatus(contract_address, admin_address, abi, wallet, private_key):
    w3 = connectToBlockchain()
    org = searchOrg_byAddress(contract_address, abi, wallet)
    id = org[1]
    if id >= 0:
        contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(admin_address)
        chain_id = 1337
        revoke = contract.functions.changeStatusofORGs(id, False).buildTransaction({"chainId": chain_id, "from": admin_address,
                                                                                    "gasPrice": w3.eth.gas_price, "nonce": nonce})
        sign_revoke = w3.eth.account.sign_transaction(
            revoke, private_key=private_key)
        send_store_contact = w3.eth.send_raw_transaction(
            sign_revoke.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(
            send_store_contact)
        return True
    else:
        return False


def revokeNewsStatus(contract_address, admin_address, abi, id, private_key):
    w3 = connectToBlockchain()
    try:
        contract = w3.eth.contract(address=contract_address, abi=abi)
        nonce = w3.eth.getTransactionCount(admin_address)
        chain_id = 1337
        revoke = contract.functions.changeStatusofNews(id, False).buildTransaction({"chainId": chain_id, "from": admin_address,
                                                                                    "gasPrice": w3.eth.gas_price, "nonce": nonce})
        sign_revoke = w3.eth.account.sign_transaction(
            revoke, private_key=private_key)
        send_store_contact = w3.eth.send_raw_transaction(
            sign_revoke.rawTransaction)
        transaction_receipt = w3.eth.wait_for_transaction_receipt(
            send_store_contact)
        return True
    except Exception as e:
        return False


def showNews(contract_address, abi):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    numNews = contract.functions.getNewsRecordsCount().call()
    lista = []
    for i in range(0, numNews):
        lista.append(contract.functions.searchNews(100000 + i).call())
    df = pd.DataFrame(lista, columns=[
                      'ID Organización', 'Nombre Organización', 'ID Noticia', 'Titulo', 'Editor', 'Veracidad'])

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
    df = pd.DataFrame(lista, columns=[
                      'ID Organización', 'Nombre Organización', 'ID Noticia', 'Titulo', 'Editor', 'Veracidad'])

    return df


def getOrgCount(contract_address, abi):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    count = contract.functions.getOrgRecordsCount().call()

    return count


def getNewsCount(contract_address, abi):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    count = contract.functions.getNewsRecordsCount().call()

    return count


def getListNewsOrg(contract_address, abi, orgId):
    w3 = connectToBlockchain()
    contract = w3.eth.contract(address=contract_address, abi=abi)
    array = contract.functions.returnORGarraywithNews(orgId).call()
    return array
