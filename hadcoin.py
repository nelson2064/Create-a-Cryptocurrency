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


# Creating a Web App
app = Flask(__name__)

#wy do we need to create such an address and scond how are we gong to create that address
#> whenever a miner mines a new block well he actually gets some kryptos that's exactly what happens for bitcoin example bitcon miner and mines your block he or she gets some bitcoins and therfore there s a transaction from the node on whcih the miner is to this miner getting the bitcoins and what is hy it is fundamental to get an address for this node  it's because whenever we mine a new block here for not the bitcon the had coin well there is going to be a tansaction from this node from the start address to yourslef (this is the first type of trnasaction there is genraal type of transaction also liee nelson to ram) 
#don't forget first transaction whenever a miner mine the new block he gets some adcoins and therefore there is a transaction from thenode to the miner
# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')  #first address of our node first node address this will be the address of the node on on port 5000         #uuid4 function form theuuid library and this is exactly how we'll create that address thsi willl generate a random address a unique address and this address will be the address of our node 

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Hadelin', amount = 1) #reciver will be the miner so the amount the miner will get 1 as the proof of work is quite easy and as recivere miner i am putting myself my name is hadelin
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200






# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json() #get the json file posted in postman 
    transaction_keys = ['sender', 'receiver', 'amount'] #all the key are present in json file #any transaction posted in postemnet must have these theree value 
    if not all(key in json for key in transaction_keys): #if some keys is missing then we give error
        return 'Some elements of the transaction are missing', 400
    
    #if transaction is okay no any key is missing
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


# Part 3 - Decentralizing our Blockchain
    

#so contractualtion for passing 1 and 2 
    #decnetralizing our blockchain our crypto currency 

#first to connect any new node you like in our decnetalized netwrok and second one to replace the cahin in any node that is not up to date on the blockchain and that is that doesn't contian the last version of the blockchain right after a new block was mine on another one 
    #we will make last 2 request and we are ready for demo

# Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():          
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET']) 
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 200




#lets test

#to make everything ready for demo and therfore we're going to prepare the json file that will need to post on post man when we interact with our blockchain to exchange some crypto currencies 

#>>>>
# so we'll have actuall two json files tomake one json file that wqill contain all the addresses of of the node and one of the json file will contain the format of a transaction you know we will prepare the right format with the right three keys sender the receiver and amount that will get something ready to post in postman
# and aslo what we will do is our servers ready and to do this will make actually three python files each of them will be connected to a differnet port one port for me one port for curial and another port for you okay i will be on post 501 cruial on 502 and you on 503

#json file are ready after this we will be ready for demo so we will be create three python files which will represent our servers of our blockchain #so our blockchain will be decnetralized netowrk of 3 nodes and so basically what we're about to do now is get this node ready

#make all node ready 
    
#lets create a cryptocurrency interacting with our blockchain in post man on our three node with you with cruel and me

#we have everything ready now the question is how are we going to do that demo well i could either test it on severla computers or i could even make a call with curial and do a live   video chat  you know with him being in austalia and receiving the adcoins in live i hingk of doing but streaming would not be that great i think and thereofre i come up with another solution which is to creat two other consoles here which is exactly like having two other computers connected to two differnet servers so lets do 5001 in one console 5002 in another 5003 in another console



#1
#first test to check you have your genesis block

#http://127.0.0.1:5001/get_chain
#http://127.0.0.1:5002/get_chain
#http://127.0.0.1:5003/get_chain


#2
#first post request to connect node with each other
#select post
  
    #http://127.0.0.1:5001/connect_node
    #http://127.0.0.1:5002/connect_node
    #http://127.0.0.1:5003/connect_node
    
    #suppose to connect 5001 node to ohter node i have to just input other node 

   # {
  #  "nodes": [
          #    "http://127.0.0.1:5002",
             # "http://127.0.0.1:5003"]
#}

#{
    #"nodes": ["http://127.0.0.1:5001",
            
          #    "http://127.0.0.1:5003"]
#}
#{
    #"nodes": ["http://127.0.0.1:5001",
            #  "http://127.0.0.1:5002"
            # ]
#}

#3
#now wer're going to test the consensus we're going to test what happens if one node we get a chain that is larger than other chain in other node
            
                #http://127.0.0.1:5001/mine_block
                #http://127.0.0.1:5001/get_chain
                
                
                
                #check in other node 
                #so if we check in other node other block may not added so 
                    #http://127.0.0.1:5002/get_chain
         #http://127.0.0.1:5003/get_chain
         
         
         
         #therfore to make same chain 
                  #http://127.0.0.1:5002/replace_chain
         #http://127.0.0.1:5003/replace_chain
         
         
         
         
         
         
         
            ##################################
    #http://127.0.0.1:5002/mine_block
    #http://127.0.0.1:5003/connect_node/mine_block