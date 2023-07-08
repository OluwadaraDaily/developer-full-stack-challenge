from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.middleware.cors import CORSMiddleware

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
  
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, crud.SECRET_KEY, algorithms=[crud.ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = schemas.TokenData(username=username)
  except JWTError:
    raise credentials_exception
  user = crud.get_user_by_username(db, username=token_data.username)
  if user is None:
    raise credentials_exception
  return user


@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
  crud.seed_users(db=db)
  crud.seed_authors(db=db)
  crud.seed_books(db=db)
  return { "message": "Database seeded successfully" }

@app.post("/token", response_model=schemas.Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
  user = crud.authenticate_user(db, form_data.username, form_data.password)
  if not user:
      raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Incorrect username or password",
          headers={"WWW-Authenticate": "Bearer"},
      )
  access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = crud.create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def get_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
  return current_user

@app.get("/users", response_model=List[schemas.User])
def fetch_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  users = crud.fetch_users(db)
  return users

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, username = user.username)
  if db_user:
    raise HTTPException(status_code=400, detail="Username already registered")
  return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id)
  return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
  response = crud.delete_user(db=db, user_id=user_id)
  return response

@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_author = crud.create_author(db=db, author=author)
  return db_author

@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author: schemas.AuthorCreate, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_author = crud.update_author(db=db, author_id=author_id, author=author)
  return db_author

@app.get("/authors", response_model=List[schemas.Author])
def fetch_authors(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  authors = crud.fetch_authors(db=db)
  return authors

@app.get("/authors/{author_id}", response_model=schemas.Author)
def get_author(author_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_author = crud.get_author(db=db, author_id=author_id)
  return db_author

@app.delete("/authors/{author_id}")
def delete_author(author_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  delete_author_response = crud.delete_author(db=db, author_id=author_id)
  return delete_author_response

@app.get("/books", response_model=List[schemas.Book])
def fetch_books(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  books = crud.fetch_books(db=db)
  return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_book = crud.get_book(db=db, book_id=book_id)
  return db_book

@app.post("/books/authors/{author_id}", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, author_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_book = crud.create_book(db=db, author_id=author_id, book=book)
  return db_book

@app.put("/books/{book_id}/authors/{author_id}", response_model=schemas.Book)
def update_book(book: schemas.BookCreate, author_id: int, book_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  db_book = crud.update_book(db=db, author_id=author_id, book=book, book_id=book_id)
  return db_book

@app.delete("/books/{book_id}/authors/{author_id}")
def delete_book(author_id: int, book_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
  delete_book_response = crud.delete_book(db=db, author_id=author_id, book_id=book_id)
  return delete_book_response