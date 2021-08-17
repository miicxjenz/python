import sqlite3
from uuid import uuid4

class VoteDB():
    def __init__(self):
        self.connect =sqlite3.connect('vote.db',check_same_thread=False)
        self.Create_table()


    def Create_table(self):
        create_topic_query =  """ CREATE TABLE IF NOT EXISTS 
        Topics 
        ( 
            id VARCHAR(64) primary key not null,
            name VARCHAR(50) not null 
        );
        """
        create_vote_query = """CREATE TABLE IF NOT EXISTS 
        Votes(
        id integer primary key AUTOINCREMENT not null,
        topic varchar(64),
        choice_name varchar(50),
        choice_count int,
        FOREIGN KEY (topic) references Topics(id)
        ) 
        """
        self.connect.execute(create_topic_query)
        self.connect.execute(create_vote_query)
        self.connect.commit() #.commit() is save


    def add_topic(self, topic_name):
        topic_id = str(uuid4())
        query =""" INSERT INTO 
        Topics (id,name) VALUES (?,?)  
        """
        # ? ป้องกันการ SQL injection

        self.connect.execute(query, (topic_id, topic_name))
        self.connect.commit()


    #สร้างที่เก็บ data
    #เขียน query ขึ้นมาอีกอันเพื่อ read database แล้วให้ vote,topic กับเรา
    def read_db_get_topic_name(self): #return is topic name / Is List of Dictionary
        """
        [
            {
                "topic_id":str,
                "topic_name":str
            }
        ]
        """
        query = """
        SELECT * FROM Topics
        """
        result = self.connect.execute(query) #.execute จะส่งค่าคืนกลับมาให้ result
        ret = [] #ret = return
        for data in result: 
            print(data)
            ret.append({
                "topic_id":data[0],
                "topic_name":data[1]
            })
        return ret


    def get_topic_id(self, topic_id):
        #มาเขียนทีหลังว่ามันจะ return เป็น [{}]
        """
        (
            [
                {(id, name, count)}
            ]

            ,Topic
        )
        """

        topic_name_query = """ 
        SELECT name FROM Topics
        WHERE Topics.id = ? 
         """
        topic_name_result = self.connect.execute(topic_name_query, (topic_id,)).fetchone() 
        #.fetchone is one result -> return is ['topic',]
        topic_name = topic_name_result[0]


        #เขียนส่วนทำงานตรงนี้ก่อน (query)
        # v is nickname of table Votes
        query = """
        SELECT id, choice_name, choice_count
        FROM Votes v 
        WHERE v.topic = ?
        """
        result = self.connect.execute(query,(topic_id,))
        ret = []
        for data in result:
            cid, cname, count = data
            ret.append((cid, cname, count))
        #print(ret)
        return ret,topic_name

    def add_choice(self, name, id):
        print("this add_choice: ", name)
        query = """
        INSERT INTO Votes(topic, choice_name, choice_count)
        VALUES (?, ?, ?);
        """
        self.connect.execute(query, (id, name, 0))
        self.connect.commit()

    def vote(self, choice_id,topic_id):
        query = """
        UPDATE Votes SET choice_count = choice_count + 1
        WHERE topic = ? and id = ?
        """
        self.connect.execute(query, (topic_id, choice_id))
        self.connect.commit()






     