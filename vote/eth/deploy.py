import json

from eth_account import Account
from solc import compile_source
from web3 import Web3, HTTPProvider

if __name__ == '__main__':
    import src
else:
    from . import src

class Deployer:

    rpc_url = "https://ropsten.infura.io/v3/49b9acbd693940a0bf84fef21253e244"

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
        construct_txn = self.Contract.constructor(16, 100, 110).buildTransaction({
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

    def vote(self, contract_address, sender_prv_key, vote_to):
        w3 = Web3(HTTPProvider(self.rpc_url))
        account = Account().privateKeyToAccount(sender_prv_key)
        contract_instance = self.Contract(contract_address)
        txn = contract_instance.functions.vote(vote_to).buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 4396860,
            'gasPrice': w3.toWei('15', 'gwei')
        })
        signed = account.signTransaction(txn)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

    def showWinner(self, contract_address):
        w3 = Web3(HTTPProvider(self.rpc_url))
        contract_instance = self.Contract(contract_address)
        return contract_instance.functions.showWinner().call()

    def endBallot (self, contract_address, sender_prv_key):
        w3 = Web3(HTTPProvider(self.rpc_url))
        account = Account().privateKeyToAccount(sender_prv_key)
        contract_instance = self.Contract(contract_address)
        txn = contract_instance.functions.endBallot().buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 4396860,
            'gasPrice': w3.toWei('15', 'gwei')
        })
        signed = account.signTransaction(txn)
        tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        print(tx_receipt)

'''
ballotContract = Deployer(16, 1573481503  , 1573481603  )
addr = ballotContract.deploy("21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74")
print(addr)
ballotContract.vote(addr, "21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74", 7)
ballotContract.endBallot(addr, "21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74")
print( ballotContract.showWinner(addr) )
'''
