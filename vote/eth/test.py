from . import config
from .interface import Deployer, BallotContract, requestGas
from eth_account import Account
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider(config.rpc_url))

account = Account.privateKeyToAccount("0x41c5c3326bb54c3fad0192672805f8e69d8d368c1545805655935d58a0db497e")
print(account.address)
b = w3.eth.getBalance(account.address)
print(b)
'''
w3 = Web3(HTTPProvider(config.rpc_url))

account = w3.eth.account.create("1234566")
pub_key = account.address
prv_key = account.privateKey.hex()

def getGasFee (_to):
    
    master_pub_key = "0x55969a2b4d94684036fa0948468B8C1D54f15FC2"
    master_prv_key = "0x41c5c3326bb54c3fad0192672805f8e69d8d368c1545805655935d58a0db497e"
    
    w3 = Web3(HTTPProvider(config.rpc_url))
    account = Account().privateKeyToAccount(master_prv_key)

    signed_txn = account.signTransaction({
        'nonce': w3.eth.getTransactionCount(account.address),
        'gas': 21000,
        'gasPrice': w3.toWei('20', 'gwei'),
        'to': _to,
        'value': w3.toWei('65952900', 'gwei')
    })

    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(pub_key, prv_key)
getGasFee(pub_key)

deployer = Deployer(16, 100, 120)
addr = deployer.deploy("0x41c5c3326bb54c3fad0192672805f8e69d8d368c1545805655935d58a0db497e")

ballotContract = BallotContract(addr, prv_key)
ballotContract.vote(7)

ballotContract = BallotContract (addr, "0x41c5c3326bb54c3fad0192672805f8e69d8d368c1545805655935d58a0db497e")
ballotContract.endBallot()
x = ballotContract.getWinner()
print(x)
'''