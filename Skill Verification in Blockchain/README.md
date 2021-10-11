# Skill Verification in Blockchain - Skillified

## Project Information

Design a skill-verification system that can help reduce the time spent on conducting competency checks, skill verification and build more trust in the skill and competency management within the organization. This can be achieved using blockchain hence the problem statement is to solve the above mentioned concern by building a blockchain based system with which the firm can be completely assured of the skills, experience, learning goal progress and the competency level of each employee along with absolute transparency on who have endorsed the employees on these skills. This information will further help the company to screen the appropriate employees for business needs.

## Implementation

 Every employee of the firm will have a profile in this web application with their verified skills listed over there. Now whenever an employee wants to add a new skill he/she will click on the add button in the UI and that will open up a dialog box. In this box there will fields like Skills to be added, Learned courses, Projects done, Other(which might include certification courses or projects done outside the firm with proper proofs like certificates or GitHub repo and so on)and Reviewer. On finishing the filling up of the fields the requester will click on the button send. Now, the request with all these details will be sent to current manager(by default) and the other reviewers(if any) added by the requester. The content will be analysed and verified by the reviewer and a acceptance notification will be sent to the requester. In case of any discrepancy the reviewer will reject the request and a rejection notification will be sent instead. On successful acceptance by the reviewer(s) the requested skill will be added to the requester’s profile.


## Install Modules

Download and install node.js for windows: https://nodejs.org/en/download/

```
npm install --global yarn
yarn global add ganache-cli (or) npm install -g ganache-cli
pip install -r requirments.txt
```

## Commands to run script

Open a terminal
```
ganache-cli --deterministic
```

Open a new terminal
```
brownie compile
brownie run ./scripts/server.py
```

## Libraries

- brownie
- sqlite
- flask

## Tech Stack

- SQL
- Solidity
- HTML/CSS/bootstrap
- Python
- Ethereum Smart Contract



