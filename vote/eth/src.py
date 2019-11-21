code = '''
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
    
    function vote (uint8 toCandidate) public {
        Voter storage voter = voters[msg.sender];
        require (!voter.voted && toCandidate <= candidates.length, "Invalid voting.");
        
        voter.voted = true;
        voter.vote = toCandidate;
        candidates[toCandidate].voteCount += 1;
        
        if (candidates[toCandidate].voteCount > winner.voteCount) {
            winner = candidates[toCandidate];
            winner_index = toCandidate;
        }
    }
    
    
    function showWinner () public view returns (uint8) {
        return winner_index;
    }
    
    function showVoteCount (uint8 candidate) public view returns (uint8 voteCount) {
        voteCount = candidates[candidate].voteCount;
    }
    
    function showVote (address voter) public view returns (uint8 voteTo) {
        voteTo = voters[voter].vote;
    }
}
'''

if __name__ == '__main__':
    pass