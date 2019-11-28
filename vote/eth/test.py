from . import config
from .interface import Deployer, BallotContract, requestGas
from eth_account import Account
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider(config.rpc_url))
master_account = Account.privateKeyToAccount(config.master)
#pub_key = account.address
#prv_key = account.privateKey.hex()

# 0x2d1C36bfdFf49290Daa4F1CC66F3a61963f6d9A2 -> 0x569519ba44a386951f7212842e4e405b2d342a14
# local address: "0x85c639212da33b0e1029f3f016b2a84f620adaae" pwd: "ballotchain"

'''
signed_txn = w3.eth.account.signTransaction(
        dict(
            nonce=w3.eth.getTransactionCount(master_account.address),
            gasPrice= w3.toWei('15', 'gwei'),
            gas = 4396860,
            to= Web3.toChecksumAddress("0x85c639212da33b0e1029f3f016b2a84f620adaae"),
            value=w3.toWei(100,'ether')
        ),
        config.master
    )
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)
'''
'''
def _requestGas(addr):
    w3 = Web3(HTTPProvider(config.rpc_url))
    w3.geth.personal.unlockAccount(Web3.toChecksumAddress("0x09cdb894965c0a4ff26309ba0964ce556a732132"), "ballotchain", 1000)
    tx_hash = w3.eth.sendTransaction({
        'from': Web3.toChecksumAddress("0x09cdb894965c0a4ff26309ba0964ce556a732132"),
        'to': addr,
        'gas': 4396860,
        'gasPrice': w3.toWei('15', 'gwei'),
        'value': w3.toWei(1,'ether')
    })
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_receipt)
'''

'''
import threading
for i in range(5):
    t = threading.Thread(target=_requestGas, args=('0x71bA9810B39a276228B7749EbdB7CA59C6a12d10',))
    t.start()
'''
x = w3.eth.getBalance(Web3.toChecksumAddress("0x6b082d847a9f469ca2eba8e19bc2d3a8c3a2dcee"))
print(w3.fromWei(x, "ether"))