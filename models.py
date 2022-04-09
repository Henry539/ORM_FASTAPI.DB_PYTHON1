from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "USERS"

    ID = Column(Integer, primary_key=True, index=True)
    USERNAME = Column(String, unique=True, index=True)
    PASSWORD = Column(String)
    STATUS = Column(Boolean, default=True)

    DATA_USER = relationship("DataUser", back_populates="OWNER")


class DataUser(Base):
    __tablename__ = "DATA_USERS"

    ID_DATA = Column(Integer, primary_key=True, index=True)
    FULLNAME = Column(String, index=True)
    AGE = Column(Integer, index=True)
    SEX = Column(Integer, index=True)
    PHONE = Column(Integer, index=True)
    USER_ID = Column(Integer, ForeignKey("USERS.ID"))

    OWNER = relationship("User", back_populates="DATA_USER")
