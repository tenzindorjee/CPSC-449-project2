# CPSC-449-project2

Tenzin Dorjee tenzin@csu.fullerton.edu: Ops

Winson Gin winsongin@csu.fullerton.edu: Dev 1 - Posting

Matthew Nguyen nmatthew45@csu.fullerton.edu: Dev 2 - Voting

### For Aggregating Voting and Posting (bff.py)
## Installation
Libraries needed to run the bff.py for aggregating voting and posting
```bash
$ pip3 install --user requests
$ sudo apt update
$ sudo apt install --yes python3-lxml
$ pip3 install --user feedgen
pip3 install Flask

```

## Usage

while the other microservices are running (refer to voting and posting read.me) 
use flask run in the terminal while in the main directory
```bash
flask run 
```
to run the bff.py

then use the following paths in your browser

```
htttp://127.0.0.1:5100/any/(amount you want) //any community based off the recent 25 

or 

http://127.0.0.1:5100/(community you want)/(amount you want) // specific community based off the recent 25

```

## Incomplete 
 - We were unable to connect the voting and posting microservices to complete bullets 3-5 for Dev 3's objectives.
