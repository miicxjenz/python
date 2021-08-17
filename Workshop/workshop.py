
import datetime                    
import hashlib                     
import json                         
from flask import Flask, jsonify    


class Blockchain:
    def __init__(self):
        self.total_bill = 0 #ข้อมูลยอดขาย
        self.chain = []
        self.create_Block(current_Hash = 1, previous_Hash = '0')

    def create_Block(self, current_Hash, previous_Hash):
        block_init = {  'index': len(self.chain) + 1,
                    'total_bill':self.total_bill,
                    'timestamp': str(datetime.datetime.now()), 
                    'proof':current_Hash,
                    'previous_hash':previous_Hash
                    #'data':
                 }
        self.chain.append(block_init)
        return block_init
    
    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_Nonce):
        new_Nonce = 1
        check_Nonce = False
        while check_Nonce is False:
            hash_operation = hashlib.sha256(str(new_Nonce**2 - previous_Nonce**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_Nonce = True
            else:
                new_Nonce += 1
        return new_Nonce

    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def Check_chain(self, chain):
        previous_block = chain[0]
        current_block = 1
        while current_block < len(chain):
            block = chain[current_block]
            if block['previousHash'] != self.hash(previous_block):
                return False
            Nonce = block['proof']
            previous_Nonce = previous_block['proof']
            hash_operation = hashlib.sha256(str(Nonce**2 - previous_Nonce**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            current_block += 1
        return True

#Create Web Application
app = Flask(__name__)

#blockchain เป็น object ของ class Blockchain:
blockchain = Blockchain()

@app.route('/mining_block', methods=['GET'])
def mining_block():
    previous_block = blockchain.get_previous_block()
    previous_Nonce = previous_block['proof']

    current_Hash = blockchain.proof_of_work(previous_Nonce)
    previous_Hash = blockchain.hash(previous_block)

    blocking = blockchain.create_Block(current_Hash, previous_Hash)
    Response ={'message':'Phuwin,you just mined a block!!!',
    'index':blocking['index'],
    'timestamp': blocking['timestamp'],
    'proof':current_Hash,
    'previousHash':previous_Hash
    }
    return jsonify(Response),200

@app.route('/update_bill', methods=['GET'])
def update_bill():
    Cost = 500000
    #blockchain = object
    #tatal_bill = การเรียกใช้ total_bill บน object จะได้ . ในการเรียกใช้
    blockchain.total_bill = blockchain.total_bill + Cost  

    previous_block = blockchain.get_previous_block()
    previous_Nonce = previous_block['proof']

    current_Hash = blockchain.proof_of_work(previous_Nonce)
    previous_Hash = blockchain.hash(previous_block)

    blocking = blockchain.create_Block(current_Hash, previous_Hash)
    Response ={'message':'Phuwin,you just mined a block!!!',
    'index':blocking['index'],
    'total_bill':blockchain.total_bill,
    'timestamp': blocking['timestamp'],
    'proof':current_Hash,
    'previousHash':previous_Hash
    }
    return jsonify(Response),200

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.Check_chain(blockchain.chain) #parameter ต้องอยู่ในรูปแบบของ object 
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

@app.route('/History_chain', methods=['GET'])
def History_chain():
    Response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)
               }
    return jsonify(Response),200

# app.run(port = 5000)

app.run(host = '0.0.0.0', port = 5000)








