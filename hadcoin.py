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
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    
    
    
    
    
    
    
    
    def add_transaction(self, sender, receiver, amount):         #amount of cryptocurrencyin this casw our crytocurrency name is adcoin
        self.transactions.append({'sender': sender,                    #the transactions will be dictionary added in the transactions list
                                  'receiver': receiver, 
                                  'amount': amount})            # defined a format of transaction
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1                  #index of the new block which is going to be created where this transsaction will go 
    
    
    
    #what is consenensus >>>    consensus is an algorithm to make sure that all the notes contain the same chain ata nay time. so whenvever block is min on any node you know welcomes new transaction that happen around the node we make sure all the ohter nodes on decentralized network are also updated with same chain 
    
    
    
    
    
    
    #method to add node 
    
           #check it in console 
   # from urllib.parse import urlparse
   # address = "http:///127.0.0.1:5000/"
   # parsed_url = urlparse(address)
   # parsed_url
   # parsed_url.netloc
    
    def add_node(self, address):           #address of node #different port for each node 
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)           #this is inof to indentify the node  127.0.0.1:5000
    
    
    
   

    # method that will replace any chain that is shorter than the longest chain among all the nodes of the network 
    #we weill call this function in a specific node and you know since each node contains a specific version of the block chain whether it is up to date or not well we will need to apply this replace chian fucntion inside a specific node 
    def replace_chain(self):
        network = self.nodes  #network variable is our set of nodes all around the world 
        longest_chain = None #we don't know which is the node have longest chain we havent scan the network yet 
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')         #so in place of node we have our address so different node have different network so we are getting the network of different node 
            if response.status_code == 200:      #check everything alright
                length = response.json()['length'] #taking length
                chain = response.json()['chain'] #taking all the chain 
                #finallt get length of the chain in differnet network 
                if length > max_length and self.is_chain_valid(chain): #our lenght is greater then maxlenght if then maxlenght is equal to length but this will run if the chain is valid if the chain is not valid we don't take that chain of that network 
                    max_length = length
                    longest_chain = chain         #updating longest chain 
        if longest_chain:                #if the longest chain is not non then it means it is updated and now 
            self.chain = longest_chain       #so the reaal chain is the longest chain
            return True#if updated true
        return False#if not false if up conditon don't match means if longest_chan is none retrun false because chain is not updated 





#now welcome to part2 and congraturlations again for developing correctly part 1 to turn this previous general purpose blockchain ito cryptocurrency 









# Part 2 - Mining our Blockchain




