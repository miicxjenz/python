from typing import Dict
from flask import Flask, request, render_template, redirect
from collections import defaultdict
from uuid import uuid4
#from db import VoteDB
from model import db, Topics, Votes

app = Flask(__name__)
#db = VoteDB()

# topic = dict({
#     'ID':{
#         'name':'Hotel',
#         'data':{'A':1,'B':0}}
# })


@app.route('/')
def index():
    #topic = db.read_db_get_topic_name()
    topic = list(Topics.select())
    #print(topic)
    return render_template("index.html", topicc=topic)




@app.route('/addTopic', methods=["POST"])
def add_new_Topic():
    #-------------------------------------------------------------------------------------
    # id = str(uuid4())
    # name = request.form.get('name')
    # topic[id] = {
    #     'name': name,
    #     'data': defaultdict(int)
    # }
    # return redirect('/')
    #-------------------------------------------------------------------------------------
    id = str(uuid4())
    name = request.form.get('name')
    #db.add_topic(topic_name=name)
    Topics.create(id = id,name =name)
    return redirect('/')
    


    

@app.route('/newTopic')
def new_Topic():
    return render_template("newTopic.html")
   


    

@app.route('/topic/<id>')
def get_Topic(id):
    #topic_data, topic_name= db.get_topic_id(topic_id = id)
    topic = list(Topics.select().where(Topics.id == id))
    votes = list(Votes.select().where(Votes.topic == topic[0]))
    #print(topic_data)
    return render_template("Topic.html",
    id = id , topics = topic[0], vote = votes)
   


    

@app.route('/topic/<id>/newChoice', methods=['POST'])
def newChoice(id):
    choice_name = request.form.get('choice')
    #db.add_choice(name=choice_name, id=id)
    Votes.create(topic = Topics.get_by_id(id), name = choice_name)
    #print("this newChoice : ",choice_name)
    return redirect(f'/topic/{id}')
   


    

@app.route('/topic/<id>/vote', methods=['POST'])
def vote_topic(id):
    choice_id = request.form.get('choice')
    #db.vote(choice_id=choice_id, topic_id= id)
    query = Votes.update(count = Votes.count +1).where(Votes.id == choice_id)
    query.execute()
    return redirect(f'/topic/{id}')
    


    

if __name__ == "__main__":
    db.connect()
    db.create_tables([Topics, Votes])
    app.run("0.0.0.0",5000)