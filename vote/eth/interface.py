import json

from eth_account import Account
from solc import compile_source
from web3 import Web3, HTTPProvider

import config

if __name__ == '__main__':
    import src
else:
    from . import src

class Deployer:

    rpc_url = config.rpc_url

    def __init__ (self, _nCandidates, _start, _end):
        self.nCandidates = _nCandidates
        self.start_time = _start
        self.end_time = _end

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
            'gas': 4396860,
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
            'gas': 4396860,
            'gasPrice': self.w3.toWei('15', 'gwei')
        })
        signed = self.account.signTransaction(txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt['status']

    def getWinner(self):
        return self.contract.functions.showWinner().call()

    def getResults(self):
        pass

    def endBallot (self):
        txn = self.contract.functions.endBallot().buildTransaction({
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gas': 4396860,
            'gasPrice': self.w3.toWei('15', 'gwei')
        })
        signed = self.account.signTransaction(txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return tx_receipt['status']

deployer = Deployer(16,1573481503, 1573481603 )
addr = deployer.deploy("21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74")
print(addr)

ballotContract = BallotContract(addr, "21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74")
ballotContract.vote(7)
ballotContract.endBallot()
print(ballotContract.getWinner())