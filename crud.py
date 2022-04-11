from sqlalchemy.orm import Session

import models


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.ID == user_id).first()


def get_user_by_name(db: Session, username: str):
    data = db.query(models.User).filter(models.User.USERNAME == username).first()
    return data

def get_all_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_all_datausers(db: Session, skip: int, limit: int):
    return db.query(models.DataUser).offset(skip).limit(limit).all()



def get_datauser(db: Session, user_id: int):
    return db.query(models.DataUser).filter(models.DataUser.USER_ID == user_id).all()

def create_user(db: Session, username: str, password: str):
    db_user = models.User(USERNAME=username, PASSWORD=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_datauser(db: Session, full_name: str, age: int, sex: str, phone: int, user_id: int):
    db_datauser = models.DataUser(FULLNAME=full_name, AGE=age, SEX=sex, PHONE=phone, USER_ID=user_id)
    db.add(db_datauser)
    db.commit()
    db.refresh(db_datauser)
    return db_datauser

