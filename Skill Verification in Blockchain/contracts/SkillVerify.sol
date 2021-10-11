// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract SkillVerify{
  
    uint256 size;
    struct Skill{
        int256 skillID;
        int256 proficiency;
        int256 learningId;
        int256 projectId;
    }

    struct SentRequests {
        int256 skill;
        int256 proficiency;
        int256 learningId;
        int256 projectId;
        int256[] reviewerIds;
        uint256 date;// date of sending
        mapping(int256 => int256) status; // mapped against the reviewerIDs
        string verdict;
    }

    struct ReceivedRequests{
        int256 senderId;
        int256 skill;
        int256 proficiency;
        int256 learningId;
        int256 projectId;
        uint256 date;//date of accpeting/rejecting
        string verdict;
        uint256 senderRequestId; //the  sent request index in the sender's profile will be stored as senderRequestID
    } 

    struct Employee {
        string name;//
        int256 empID;
        string email;//
        int256 workExperience;//
        string password;//
        Skill[] skills;        
        SentRequests[] sentRequests;
        ReceivedRequests[] receivedRequests;
    }
    
    Employee[] public employee;
    mapping(int256 => Employee) public employeeMap;

    function register( int256 _empID) public{
        // adding the new employee to the array of employees
        employee.push();
        employee[employee.length -1].empID = _empID;  

        // registering the employee details against the employee ID in the mapping
        employeeMap[_empID].empID = _empID;
    }
    
    
    function initiateRequest(int256 _senderId, int256 _skillID, int256 _proficiency, int256 _learning_id, int256 _project_id, int256[] memory _receivers) public{
        Employee storage sender = employeeMap[_senderId];

        uint256 _date = block.timestamp;

        // update sent request of sender
        sender.sentRequests.push();// a way to push a new entry into arrays containing mappings and etc.
        sender.sentRequests[sender.sentRequests.length -1].skill = _skillID;
        sender.sentRequests[sender.sentRequests.length -1].proficiency = _proficiency;
        sender.sentRequests[sender.sentRequests.length -1].learningId = _learning_id;
        sender.sentRequests[sender.sentRequests.length -1].projectId = _project_id;
        sender.sentRequests[sender.sentRequests.length -1].reviewerIds = _receivers;
        sender.sentRequests[sender.sentRequests.length -1].date = _date;
        sender.sentRequests[sender.sentRequests.length -1].verdict = "Pending";
        

        ReceivedRequests memory _receivedRequest;
        _receivedRequest.senderId = _senderId;
        _receivedRequest.skill = _skillID;
        _receivedRequest.proficiency = _proficiency;
        _receivedRequest.learningId = _learning_id;
        _receivedRequest.projectId = _project_id;
        _receivedRequest.date = _date;
        _receivedRequest.verdict = "Pending";
        // assigning the index number of the request in sentRequests list of that sender as the Sent Request ID in the receiver's recievedrequest 
        _receivedRequest.senderRequestId = sender.sentRequests.length -1;

        // update request on receivers
        for(uint256 i=0; i<_receivers.length;i++){
            sender.sentRequests[sender.sentRequests.length -1].status[_receivers[i]] = 0;
            employeeMap[_receivers[i]].receivedRequests.push(_receivedRequest); 
        }
    }
    
    function validateRequest(int _verdict, int256 _reviewerId, uint256 _requestIndex) public{
        
        Employee storage reviewer = employeeMap[_reviewerId];
        Employee storage requester = employeeMap[reviewer.receivedRequests[_requestIndex].senderId];

        reviewer.receivedRequests[_requestIndex].date = block.timestamp;  // date of acceptance/rejection

        if(_verdict==1){
            // update reviewer status
            reviewer.receivedRequests[_requestIndex].verdict = "Accepted";

            // update requester skill
            requester.sentRequests[reviewer.receivedRequests[_requestIndex].senderRequestId].status[reviewer.empID] = 1;
        }
        else{
            reviewer.receivedRequests[_requestIndex].verdict = "Rejected";
            requester.sentRequests[reviewer.receivedRequests[_requestIndex].senderRequestId].status[reviewer.empID] = -1;
        }
        refresh(reviewer.receivedRequests[_requestIndex].senderId, reviewer.receivedRequests[_requestIndex].senderRequestId);
    }


    function refresh(int256 _empID, uint index) public {
        Employee storage temp = employeeMap[_empID];
        int256[] memory reviewerIds = temp.sentRequests[index].reviewerIds;
        mapping(int256 => int256) storage status = temp.sentRequests[index].status;
        uint accept;uint reject;
        for(uint i=0; i < reviewerIds.length; i++){
            if(status[reviewerIds[i]] == 1)
                accept+=1;
            else if(status[reviewerIds[i]]==-1)
                reject+=1;
        }
        uint acceptPercentage = (accept*100)/reviewerIds.length;
        uint rejectPercentage = (reject*100)/reviewerIds.length;
        if(acceptPercentage > 50){
            employeeMap[_empID].skills.push(Skill(temp.sentRequests[index].skill, temp.sentRequests[index].proficiency, temp.sentRequests[index].learningId, temp.sentRequests[index].projectId));
            employeeMap[_empID].sentRequests[index].verdict = "Accepted";
        }
        else if(rejectPercentage > 50)
            employeeMap[_empID].sentRequests[index].verdict = "Rejected";
    }    


    function retrieve(int256 _empID) public view returns( int256[] memory, int256[] memory, int256[] memory, int256[] memory) {
        Employee storage temp = employeeMap[_empID];
        uint length = temp.skills.length;
        int256[] memory skill = new int256[](length);
        int256[] memory proficiency = new int256[](length);
        int256[] memory learningId = new int256[](length);
        int256[] memory projectId = new int256[](length);
        
        // need changes- need to returns all the skillIds
        for(uint i=0; i < temp.skills.length; i++){
            skill[i] = temp.skills[i].skillID;
            proficiency[i] = temp.skills[i].proficiency;
            learningId[i] = temp.skills[i].learningId;
            projectId[i] = temp.skills[i].projectId;
        }
        
        return ( skill, proficiency, learningId, projectId) ;
    }

    function retrieveSentRequests(int256 _empID, uint index) public view returns(int , int, int , int, uint, string memory){
        Employee storage temp = employeeMap[_empID];
        int skill = temp.sentRequests[index].skill;
        int proficiency = temp.sentRequests[index].proficiency;
        int learningId = temp.sentRequests[index].learningId;
        int projectId = temp.sentRequests[index].projectId;
        uint date = temp.sentRequests[index].date;
        string memory verdict = temp.sentRequests[index].verdict;
        return (skill, proficiency, learningId, projectId, date, verdict);
    }

    function retrieveReceivedRequests(int256 _empID, uint index) public view returns(int , int, int, int, int, uint, string memory) {
        Employee storage temp = employeeMap[_empID];
        // int skill = temp.receivedRequests[index].skill;
        // int proficiency = temp.receivedRequests[index].proficiency;
        // int learningId = temp.receivedRequests[index].learningId;
        // int projectId = temp.receivedRequests[index].projectId;
        // int256 senderId = temp.receivedRequests[index].senderId;
        uint date = temp.receivedRequests[index].date;
        string memory verdict = temp.receivedRequests[index].verdict;
        return (temp.receivedRequests[index].senderId, temp.receivedRequests[index].skill, temp.receivedRequests[index].proficiency, temp.receivedRequests[index].learningId, temp.receivedRequests[index].projectId, date, verdict);
    }

    // function getPassword(int256 _empID) public view returns(string memory){
    //     Employee storage temp = employeeMap[_empID];
    //     return (temp.password);
    // }

    function getReceivedRequestsLength(int256 _empID) public view returns(int256){
        Employee storage temp = employeeMap[_empID];
        return int256(temp.receivedRequests.length);
    }
      
    function getSentRequestsLength(int256 _empID) public view returns(int256){
        Employee storage temp = employeeMap[_empID];
        return int256(temp.sentRequests.length);
    }

    function getEmployeeIds() public view returns(int256[] memory) {
        uint length = employee.length;
        int256[] memory empId = new int256[](length);
        for(uint i=0; i < length; i++)
            empId[i] = employee[i].empID;
        return empId;
    }
}