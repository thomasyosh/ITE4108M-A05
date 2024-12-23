from peewee import *
import os
import datetime

db_type = os.getenv("DATABASE_TYPE")
db_connection = None
local_db = os.getenv("LOCAL_DB")

if local_db == "false":
    if db_type == "postgres":
        db_connection = PostgresqlDatabase(
            os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            host=os.getenv("POSTGRES_HOST"),
            password=os.getenv("POSTGRES_PASSWORD")
            )
    elif db_type == "mysql":
        db_connection = MySQLDatabase(
            os.getenv("MYSQL_DB"),
            user=os.getenv("MYSQL_USER"),
            host=os.getenv("MYSQL_HOST"),
            password=os.getenv("MYSQL_PASSWORD")
        )
else:
    db_connection = PostgresqlDatabase(
            os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            host="localdb",
            password=os.getenv("POSTGRES_PASSWORD")
            )
    


class NullTextField(TextField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('null', True)
        super(NullTextField, self).__init__(*args, **kwargs)

class BaseModel(Model):
    pk_id = AutoField()
    created_date = DateTimeField(default=datetime.datetime.now)
    modified_date = DateTimeField(null = True)
    is_active = BooleanField(default=True)
    
    class Meta:
        database = db_connection

    @classmethod
    def update(cls, *args, **kwargs):
        kwargs["modified_date"] = datetime.datetime.now()
        return super(BaseModel,cls).update(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.created_date = datetime.datetime.now()
        return super(BaseModel,self).save(*args, **kwargs)
    
    @classmethod
    def fieldnames(cls) -> list[str]:
        return [f.name for f in cls.fields()]
    
    @classmethod
    def fields(cls) -> list[Field]:
        print("Override method for <BaseModel.fields> not implemented!")
        return []

class Testing(BaseModel):    
    name = NullTextField()

class User(BaseModel):
    name = TextField(null = True)
    telephone = TextField(null = True)
    password = TextField(null = True)

try:
    db_connection.create_tables([Testing, User])
    
except Exception as e:
    print ("Database connection error")