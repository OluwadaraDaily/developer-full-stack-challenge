from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing_extensions import Annotated
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



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

@app.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
  db_user = crud.get_user(db, user_id)
  return db_user