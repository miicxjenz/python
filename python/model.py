from peewee import *

db = SqliteDatabase('vote_orm.db')

class BaseModel(Model):
    class Meta:
        database=db
        
class Topics(BaseModel):
    id = CharField(max_length=60,null=False,primary_key=True)
    name=TextField()

class Votes(BaseModel):
    id=AutoField(null=False,primary_key=True)
    topic = ForeignKeyField(Topics,backref='topic')
    name=TextField()
    count=IntegerField(default=0)
