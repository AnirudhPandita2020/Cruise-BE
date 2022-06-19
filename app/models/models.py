from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey, Boolean
from .database import Base
from sqlalchemy.orm import relationship


class Owner(Base):
    __tablename__ = "owner"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Systems(Base):
    __tablename__ = "System"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    added_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=('now()'))
    ownerid = Column(Integer, ForeignKey("owner.id", ondelete="CASCADE"), nullable=False)
    in_user = Column(Boolean, nullable=False, server_default='False')
    owner = relationship("Owner")


class User(Base):
    __tablename__ = "user"
    name = Column(String, nullable=False)
    phone = Column(String(length=10), nullable=False, primary_key=True)
    system_id = Column(Integer, ForeignKey('System.id', ondelete="CASCADE"), nullable=False)
    startTime = Column(String, nullable=False)
    endTime = Column(String, nullable=False)


class History(Base):
    __tablename__ = "History"
    name = Column(String, nullable=False)
    systemid = Column(Integer, ForeignKey('System.id', ondelete="CASCADE"), primary_key=True, nullable=False)
    phone = Column(Integer, ForeignKey('user.phone', ondelete="CASCADE"), nullable=False, primary_key=True)
    ownerid = Column(Integer, nullable=False)
