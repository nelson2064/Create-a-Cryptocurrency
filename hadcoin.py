# Module 2 - Create a Cryptocurrency

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4: pip install requests==2.18.4

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse



#general purpose blockchain into crypto currency 
#> what makes a blockchain a cryptocurrency the answer is transaction the principle of a cryptocurrency is that we're able to exchange these crypto currency thought transactions that are secured added to new blocks mines by the miners in the most secure way that once some transactions are added to a new block the block isintegrated to the block chain and its impossible to modify anything in the blockchain  
#Consensus in blockchain refers to the process by which multiple nodes on a network agree on the current state of the blockchain ledger. This is necessary to ensure that all nodes have the same version of the ledger and to prevent any fraudulent or malicious activity. In other words, consensus is the mechanism that enables trustless, decentralized systems like blockchain to function.
############################first##################
#1.adding the transaction 2.making the consensus


# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = [] #all the transaction contains in this list  #before adding  to the block before creating block  we have to store some where so we are stroing in a list
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions} 
        #after creating a new block in new block new transaction will came so making the transaciton empty
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
 



