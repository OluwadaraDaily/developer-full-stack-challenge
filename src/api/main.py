from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
  print(f'FORM DATA -> {form_data.username}')
  user_dict = crud.get_user_by_username(db, username=form_data.username)
  print(f'USER ID -> {user_dict.id}')
  new_user_dict = { "username": user_dict.username, "password": user_dict.password }
  if not user_dict:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
  user = schemas.UserCreate(**new_user_dict)
  print(f'USER 2 -> {user}')
  is_password_verified = crud.validate_user_password(db=db, username=user_dict.username, password=user_dict.password)

  print(f'IS_PWD_VERIFIED -> {is_password_verified}')
  if not is_password_verified:
    raise HTTPException(status_code=400, detail="Incorrect username or password")
  
  return {"access_token": user.username, "token_type": "bearer"}

def fake_decode_token(token):
  return schemas.User(
      username=token + "fakedecoded"
  )

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
  print(f"Token ->{token}")
  user = fake_decode_token(token)
  if not user:
    raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="Invalid authentication credentials",
          headers={"WWW-Authenticate": "Bearer"},
        )
  return user

@app.get("/users/me")
def get_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
  return current_user

@app.get("/users", response_model=List[schemas.User])
def fetch_users(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db), offset: int = 0, limit: int = 100):
  users = crud.fetch_users(db, offset=offset, limit=limit)
  response = {
    "token": token,
    "data" : users
  }
  return response

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
  db_user = crud.get_user_by_username(db, username = user.username)
  if db_user:
    raise HTTPException(status_code=400, detail="Username already registered")
  return crud.create_user(db=db, user=user)