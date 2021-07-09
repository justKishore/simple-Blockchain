# Creating simple BlockChain

# To be installed:
# Flask==0.12.2 : pip install Flask==0.12.2
# postman HTTP client :https://www.getpostman.com/



import datetime #for time stamp
import hashlib #used to hash block
import json #used function inside it to encode the blocks before we hash them
from flask import Flask,jsonify #Flask for creating web application 
                                 #jasonify fn for returning messages in postman,
                                 # when we interact with our blockchain

# Building a Blockchain using class


class BlockChain :
    
    def __init__(self):
        self.chain=[]
        self.create_block(proof = 1, previous_hash='0') #it will be Genesis Block
        
    def create_block(self, proof, previous_hash):
        block={'index': len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof': proof,
               'previous_hash': previous_hash} 
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self,previous_proof):
        new_proof= 1
        check_proof= False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2- previous_proof **2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    
    def hash(self,block):
        #json lib we use dumps function to convert object into string
        #we take dumps function  not str function because in part 2 we put 
        #our blocks dictionaries into a json file/format
        
        encoded_block = json.dumps(block, sort_keys=True).encode() #sortkey = true so they are sorted by keys
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index < len(chain):
            block=chain[block_index]
            if block['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2- previous_proof **2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Mining Blockchain

app = Flask(__name__)    #creating web app using flask
#app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False #to avoid internal server error
blockchain = BlockChain() #object of Blockchain Class 
@app.route('/mine_block',methods=['GET'])

def mine_block() :
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Cheers, Block Mined!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response),200 

# Getting Full Blockchain 
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain' :blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response),200

#run app 
#check flask documentation to know about host and port
app.run(host = '0.0.0.0',port =5000)
    
    
    
            
    
    
               
               
               
               
               
               
    






