import json

from eth_account import Account
from solc import compile_source
from web3 import Web3, HTTPProvider

source_code = '''
pragma solidity >=0.4.22 <0.6.0;
contract Ballot {

    struct Voter {
        bool voted;
        uint8 vote;
    }
    
    struct Candidate {
        uint8 voteCount;
    }
    
    mapping (address => Voter) voters;
    
    Candidate[] candidates;
    uint start_time;
    uint end_time;
    
    Candidate winner;
    uint8 winner_index;
    
    constructor (uint8 _numCandidates, uint _start_time, uint _end_time) public {
        candidates.length = _numCandidates;
        start_time = _start_time;
        end_time = _end_time;
    }
    
    modifier onlyAfterEnd {
        require (now >= end_time, "Ballot is not finished");
        _;
    }
    
    function vote (uint8 toCandidate) public {
        Voter storage voter = voters[msg.sender];
        require (!voter.voted && toCandidate <= candidates.length, "Invalid voting.");
        require (now < end_time, "Ballot is finished");
        
        voter.voted = true;
        voter.vote = toCandidate;
        candidates[toCandidate].voteCount += 1;
        
        if (candidates[toCandidate].voteCount > winner.voteCount) {
            winner = candidates[toCandidate];
            winner_index = toCandidate;
        }
    }
    
    
    function showWinner () onlyAfterEnd public view returns (uint8) {
        return winner_index;
    }
    
    function showVoteCount (uint8 candidate) onlyAfterEnd public view returns (uint8 voteCount) {
        voteCount = candidates[candidate].voteCount;
    }
    
    function showVote () onlyAfterEnd public view returns (uint8 voteTo) {
        voteTo = voters[msg.sender].vote;
    }
}
'''

class Deployer:

    rpc_url = "https://ropsten.infura.io/v3/49b9acbd693940a0bf84fef21253e244"

    def __init__ (self, _nCandidates, _start, _end):
        self.nCandidates = _nCandidates
        self.start_time = _start
        self.end_time = _end

    def deploy (self, prv_key):
        w3 = Web3(HTTPProvider(self.rpc_url))
        account = Account().privateKeyToAccount(prv_key)

        # Compile source
        compiled_sol = compile_source (source_code)
        contract_interface = compiled_sol["<stdin>:Ballot"]
        Contract = w3.eth.contract (
            abi = contract_interface['abi'],
            bytecode = contract_interface['bin'], 
            bytecode_runtime = contract_interface['bin-runtime']
        )

        # Make transaction
        construct_txn = Contract.constructor(16, 100, 110).buildTransaction({
            'from': account.address,
            'nonce': w3.eth.getTransactionCount(account.address),
            'gas': 3000000,
            'gasPrice': w3.toWei('15', 'gwei')
        })

        # sign transaction
        signed = account.signTransaction(construct_txn)

        # send transaction
        address = w3.eth.sendRawTransaction(signed.rawTransaction)

        print(address.hex())