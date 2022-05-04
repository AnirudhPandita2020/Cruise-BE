
from sqlalchemy import Column, Integer, String,TIMESTAMP,text,ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    username =Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    

class Systems(Base):
    __tablename__ = "systems"
    id = Column(Integer,nullable = False,primary_key = True,autoincrement=True)
    name = Column(String,nullable = False)
    added_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=('now()'))
    ownerid = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")