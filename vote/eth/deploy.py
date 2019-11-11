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

'''
class BallotContract:

    this.rpc_url = "https://ropsten.infura.io/v3/49b9acbd693940a0bf84fef21253e244"

    def __init__ (private_key, _nCandidates, _start, _end):
        this.nCandidates = _nCandidates
        this.start_time = _start
        this.end_time = _end

'''
compiled_sol = compile_source (source_code)

#rpc_url = "http://www.ballotchain.net:8805"
rpc_url = "https://ropsten.infura.io/v3/49b9acbd693940a0bf84fef21253e244"
w3 = Web3(HTTPProvider(rpc_url))

account = Account()
acct = account.privateKeyToAccount("21DF8E8466D4C5B11BE3E1890C45C99A290BC3D7388151CC658BC35885D50F74")
contract_interface = compiled_sol["<stdin>:Ballot"]

Ballot = w3.eth.contract(
    abi = contract_interface['abi'], 
    bytecode = contract_interface['bin'], 
    bytecode_runtime = contract_interface['bin-runtime']
)

construct_txn = Ballot.constructor(16, 100, 110).buildTransaction({
    'from': acct.address,
    'nonce': w3.eth.getTransactionCount(acct.address),
    'gas': 3000000,
    'gasPrice': w3.toWei('15', 'gwei')
})

signed = acct.signTransaction(construct_txn)

res = w3.eth.sendRawTransaction(signed.rawTransaction)

print(res.hex())