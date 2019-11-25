from . import config
from .interface import Deployer, BallotContract, requestGas
from eth_account import Account
from web3 import Web3, HTTPProvider

w3 = Web3(HTTPProvider(config.rpc_url))
account = Account.privateKeyToAccount(config.master)
pub_key = account.address
prv_key = account.privateKey.hex()

balance = w3.eth.getBalance(pub_key)
eth_amount = w3.fromWei(balance, 'ether')

print(eth_amount)