import json
import requests

from eth_account import Account
from solc import compile_source
from web3 import Web3, HTTPProvider

from . import src
from . import config


def makeConnection ():
    def checkConnection(idx):
        try:
            response = requests.get(config.connection_pool[idx]['rpc_url'])
            return True 
        except(requests.exceptions.ConnectionError):
            pass
        return False

    for i in range(len(config.connection_pool)):
        ret = checkConnection(i)
        if (ret == True):
            config.rpc_url = config.connection_pool[i]['rpc_url']
            config.coinbase = config.connection_pool[i]['coinbase']
            print("Connect to node ", i + 1)
            return True
    return False

# Request gas from faucet
def requestGas (pub_key):

    def _requestGas(addr):
        coinbase = config.coinbase
        w3 = Web3(HTTPProvider(config.rpc_url))
        w3.geth.personal.unlockAccount(Web3.toChecksumAddress(coinbase), "ballotchain", 1000)
        tx_hash = w3.eth.sendTransaction({
            'from': Web3.toChecksumAddress(coinbase),
            'to': addr,
            'gas': 3840930,
            'gasPrice': w3.toWei('15', 'gwei'),
            'value': w3.toWei(1,'ether')
        })
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    # init web3
    w3 = Web3(HTTPProvider(config.rpc_url))

    # Check balance of pub_key
    balance = w3.eth.getBalance(pub_key)
    eth_amount = w3.fromWei(balance, 'ether')

    # If user have already much ehter, pass
    if (eth_amount >= 0.8):
        print("Enough gas to: ", pub_key)
        return 1
    # else, request user from faucet
    else:
        _requestGas(pub_key)
        return 1
    '''
    else:
        res = requests.post(config.faucet_url, data=pub_key, headers={'Content-Type': 'text/plain'})
        if (res.status_code == 200):
            w3.eth.waitForTransactionReceipt(res.text)
            return 1
        else:
            return 0
    '''
    
class Deployer:

    def __init__ (self, _nCandidates, _start, _end):
        self.nCandidates = _nCandidates
        self.start_time = _start
        self.end_time = _end
        self.rpc_url = config.rpc_url

        # Compile source
        w3 = Web3(HTTPProvider(self.rpc_url))

        compiled_sol = compile_source (src.code)
        contract_interface = compiled_sol["<stdin>:Ballot"]
        
        self.Contract = w3.eth.contract (
            abi = contract_interface['abi'],
            bytecode = contract_interface['bin'], 
            bytecode_runtime = contract_interface['bin-runtime']
        )

    def deploy (self, prv_key):
        w3 = Web3(HTTPProvider(self.rpc_url))
        account = Account().privateKeyToAccount(prv_key)
       
        # Make transaction
        construct_txn = self.Contract.constructor(self.nCandidates, self.start_time, self.end_time).buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 3840930, #4396860,
            'gasPrice': w3.toWei('15', 'gwei')
        })

        # sign transaction
        signed = account.signTransaction(construct_txn)

        # send transaction
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        address = tx_receipt['contractAddress']

        return address

class BallotContract:
    def __init__ (self, _address, sender_prv_key):
        # Compile source code
        self.w3 = Web3(HTTPProvider(config.rpc_url))
        compiled_sol = compile_source (src.code)
        contract_interface = compiled_sol["<stdin>:Ballot"]
        
        # Build contract factory
        Contract = self.w3.eth.contract (
            abi = contract_interface['abi'],
            bytecode = contract_interface['bin'], 
            bytecode_runtime = contract_interface['bin-runtime']
        )

        # Get contract instance
        self.contract = Contract(_address)

        # unlock account
        self.account = Account().privateKeyToAccount(sender_prv_key)
        
    def vote(self, vote_to):
        txn = self.contract.functions.vote(vote_to).buildTransaction({
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gas': 3840930, #4396860,
            'gasPrice': self.w3.toWei('45', 'gwei')
        })
        signed = self.account.signTransaction(txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)
        return tx_receipt
        
    def getWinner(self):
        return self.contract.functions.showWinner().call()

    def getVoteCount(self, idx):
        return self.contract.functions.showVoteCount(idx).call()
