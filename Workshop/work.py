###########################
#### Create Blockchain ####
###########################
"""
To be installed
    # Flask: pip install Flask
    # Postman HTTP Client: http://www.getpostman.com/
"""


import datetime                     #_library datetime ทำให้ทราบถึงวัน-เวลา
import hashlib                      #_Generate hash by library hashlib
import json                         #_ส่งข้อมูล Webserver ในรูปแบบของ json
from flask import Flask, jsonify    #_import Flask and jsonify

###################################
# Part 1 - Building a Blockchain #
###################################
#_ การเขียน blockchain ให้ทำงานได้หลากหลายและเก็บข้อมูลได้เยอะ  -> Must! Create Class

class Blockchain:
    def __init__(self):
        #_สร้าง chain
        self.chain = [] #_block genesis ตอนแรกก็จะยังไม่มี previous hash -> Give chain is empty list
        self.create_Block(proof = 1, previous_Hash = '0') #สร้าง block เรียกใช้ fc ก่อนเดี๋ยวไปสร้างทีหลัง
        #_Parameter: 1.proof = Nonce 
        #            2.previous_Hash

    #_Create function change block
    #_INput parameter = proof, previous_Hash
    def create_Block(self, proof, previous_Hash):
        #_create dictionary block 
        #_ตอนแรก self.chain = 0 เราเลย +1 เพื่อให้ index = 1
        block0 = {'index': len(self.chain) + 1,  #index is ตัวเลขลำดับของ block
        'timestamp': str(datetime.datetime.now()), #มันจะ stamp time(current time) at the time Mining block or Create block
        'proof':proof,
        'previous_Hash':previous_Hash
        #'data':
        }
        #_Connect previous block
        self.chain.append(block0)
        return block0

##########################
#### Test blockchain #####
##########################
#block = Blockchain()
#print("Gensis Block")   #Show genesis block
#_Show built-in create_Block()
#_Show index 0
#print(block.chain[0]['index'])    
#print(block.chain[0]['timestamp']) 
#print(block.chain[0]['proof'])  
#print(block.chain[0]['previous_Hash']) 

#_สร้างเพิ่มอีก block
#block.create_Block(proof = 1, previous_Hash = 'test')
#_Show index 1
#print('--------------')
#print(block.chain[1]['index'])    
#print(block.chain[1]['timestamp']) 
#print(block.chain[1]['proof'])  
#print(block.chain[1]['previous_Hash']) 

    ###############################
    #### Check previous Block #####
    ###############################

    #_Create funtion get previous block
    #_Don't have Input parameter 
    def get_previous_block(self): #เพื่อให้ check ว่า block ล่าสุดมี hash คืออะไร?
        #_python สามารถเข้าถึง list ล่าสุดได้ด้วยคำสั่งของ python คือ index  -1
        return self.chain[-1]

    ########################
    #### Proof of Work #####
    ########################
    #_INput parameter = previous_proof
    def proof_of_work(self, previous_proof): #previous_proof = previous Nonce
        #_previous_proof = Mining(กำหนดโจทย์คณิตศาสตร์) give to Miner search Hash
        #_Mining = search Nonce or new_proof
        new_proof = 1 #ให้เพิ่มขึ้นทีละ 1 จนกว่าจะได้ hash ที่ตรงตาม target ที่ตั้งไว้
        
        check_proof = False
        while check_proof is False:
            #_กำหนด operation of hash -> parameter is โจทย์ทางคณิตศาสตร์
            hash_operation = hashlib.sha256( str(new_proof**2 - previous_proof**1).encode()).hexdigest()
            #_ .hexdigest() แยกตัวอักษร & convert to ฐาน16

            if hash_operation[:4] == '0000': 
            #_Trick! to set target of hash
            #_if hash ใด return ค่าออกมาตัวข้างหน้าไม่เป็น 0000 ก็จะไม่ให้มัน proof
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    ###############################
    ############# Hash ############
    ###############################
    #_ต้องการทราบถึง hash เพื่อที่จะส่ง hash ด้วย pass server
    #_code = server ในการติดต่อสื่อสารกับ client โดยใช้การส่งในรูปแบบ json
    #_INput parameter = block
    def hash(self,block):
        #convert block ให้อยู่ในรูปแบบ json โดยใช้คำสั่ง dumps
        #_sort_keys = เรียงลำดับ keys ที่อยู่ใน dictionary
        #_เมื่อกี้ที่เรา proof of work เสร็จแล้ว
        #_เราจะนำมาใช้ร่วมกับ hash() โดยการ get ค่า hash หลังจากที่เรา proof of work เสร็จแล้ว
        #_โดย block ที่เราทำการ proof เสร็จแล้วจะเอามาเป็น input of hash() for get hash value
        #_โดยจะ return  hash โดยการเอา encode_block ไปใส่ใน hash แล้วทำให้เป็นเลขฐาน16
        encode_block = (json.dumps(block, sort_keys = True).encode()).hexdigest()
        return hashlib.sha256(encode_block)

###############################
######### Library json ########
###############################
#_การเข้าถึงค่า hash ที่มันเกิดการ proof ขึ้นมา
# blockchain = Blockchain() #_เรียก Class Blockchain

#_Test create
#_ตอนที่เรียกใช้ class Blockchain มันก็จะสร้าง genesis class มาให้ Auto 
#_เพราะ self.create_Block(proof = 1, previous_Hash = '0')
# blockchain.create_Block(True,'')
#_print เพื่อดู hash  -> input parameter ต้องเป็น block
#_input parameter = Dictionary in list
# print(blockchain.hash(blockchain.chain[0])) #_block 0

### json ###
#_ json(JavaScript Object Notation) is format of JavaScript
#_ format ที่ไว้ติดต่อกันระหว่าง server with client

# import json
# print(json.dumps({"a": 1, "c": 4, "b": 2}, sort_keys=True))

    ###############################
    ######## Check Hash ###########
    ###############################
    def Check_chain(self, chain): 
        #_chain is list contain dictionary
        previous_block = chain[0]
        #update index block
        block_index = 1
        while block_index < len(chain): #_len(chain) is current block index
            blockk = chain[block_index]
            #_check ว่า blockk['key'] == hash ที่จากได้ function hash หรือเปล่า?
            #_ self.hash() is called function in class
            if blockk['previous_Hash'] != self.hash('previous_Hash'): #ปกติมันต้องเท่ากัน 
                return False
            previous_proof = previous_block['proof']
            proof = blockk['proof']
            hash_operation = hashlib.sha256( str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False 
            previous_block = blockk
            block_index += 1
        return True

###################################
# Part 2 - Mining our Blockchain  #
###################################

#Create Web Application
app = Flask(__name__)

#Creating Blockchain (Object)
blockchain = Blockchain()

@app.route('/mining_block', methods=['GET'])
def mining_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)

    previous_hashh = blockchain.hash(previous_block)
    #สร้าง function hash เพื่อเก็บค่า hash 

    blocking = blockchain.create_Block(proof, previous_hashh)

    Response ={'message':'Phuwin,you just mined a block!!!',
    'index':blocking['index'],
    'timestamp': blocking['timestamp'],
    'proof':proof,
    'previous_Hash':previous_hashh
    }
    return jsonify(Response),200

@app.route('/History_chain', methods=['GET'])
def History_chain():
    Response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)
               }
    return jsonify(Response),200

app.run(host = '0.0.0.0', port = 5000)