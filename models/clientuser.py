from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text as sa_text
from db.db import db
import uuid




class ClientUser(db.Model):
    __tablename__ = "client_users"

    id = Column(db.Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    uname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    verified=Column(Integer,default=0,nullable=False)

    def __init__(self,uname,email,password):
        self.uname=uname
        self.email=email
        self.password=password

        
    def __repr__(self):
        return f"Name : {self.uname}, ID :{self.id}"
    
class OpsUser(db.Model):
    __tablename__ = "ops_users"

    id = Column(db.Text(length=36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opsname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
