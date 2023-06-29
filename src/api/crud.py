import models
import bcrypt
from sqlalchemy.orm import Session

import schemas

def fetch_users(db: Session, offset: int = 0, limit: int = 100):
  return db.query(models.User).offset(offset).limit(limit).all()

def get_user(db: Session, user_id: int):
  return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def validate_user_password(db: Session, username: str, password: str):
  user = get_user_by_username(db=db, username=username)
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  # salt = user.password.find(bcrypt.gensalt())
  # user_password = user.password
  print("PASSWORD ->", password)
  print(f'USER PASSWORD ->', user.password)

  check = bcrypt.checkpw(password.encode('utf-8'), user.password)
  print(f'Check ->', check)

  # print(f'HASHED PASSWORD ->', hashed_password)
  return user.password == hashed_password

def create_user(db: Session, user: schemas.UserCreate):
  hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
  db_user = models.User(username = user.username, password = hashed_password.decode('utf8'))
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

