import models
import bcrypt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "affd16f38420f41a19094732d9288056a094e56ed0adb9191e84317bd6317be7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def fetch_users(db: Session, offset: int = 0, limit: int = 100):
  return db.query(models.User).offset(offset).limit(limit).all()

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
  return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
  user = get_user_by_username(db, username)
  if not user:
      return False
  if not verify_password(password, user.password):
      return False
  return user

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
  db_user = models.User(username = user.username, password = hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

def fetch_authors(db: Session, offset: int = 0, limit: int = 20):
  return db.query(models.Author).offset(offset).limit(limit).all()

def fetch_books(db: Session, offset: int = 0, limit: int = 20):
  return db.query(models.Book).offset(offset).limit(limit).all()

def get_book(db: Session, book_id: int):
  return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_author(db: Session, author_id: int):
  return db.query(models.Author).filter(models.Author.id == author_id).first()

def fetch_author_books(db: Session, author_id: int, offset: int = 0, limit: int = 20):
  return db.query(models.Book).filter(models.Book.author_id == author_id).offset(offset).limit(limit).all()

def get_book_author(db: Session, book_id: int):
  book = get_book(db, book_id)
  return db.query(models.Author).filter(models.Author.id == book.author_id).first()

def create_book(db: Session, book: schemas.BookCreate, author_id: int):
  db_book = models.Book(**book.dict(), author_id = author_id)
  db.add(db_book)
  db.commit()
  db.refresh(db_book)
  return db_book

def create_author(db: Session, author: schemas.AuthorCreate):
  db_author = models.Author(**author.dict())
  db.add(db_author)
  db.commit()
  db.refresh(db_author)
  return db_author

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
  to_encode = data.copy()
  if expires_delta:
      expire = datetime.utcnow() + expires_delta
  else:
      expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt
