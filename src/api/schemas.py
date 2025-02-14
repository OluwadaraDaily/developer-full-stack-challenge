from typing import List, Union

from pydantic import BaseModel

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
  password: str

class User(UserBase):
  id: int

  class Config:
    orm_mode = True

class BookBase(BaseModel):
  name: str
  pages: int

class BookCreate(BookBase):
  pass

class Book(BookBase):
  id: int
  author_id: int

  class Config:
    orm_mode = True


class AuthorBase(BaseModel):
  name: str

class AuthorCreate(AuthorBase):
  pass

class Author(AuthorBase):
  id: int
  books: List[Book] = []

  class Config:
    orm_mode = True

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  username: Union[str, None] = None