from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, BigInteger, LargeBinary
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
  __tablename__ = 'users'
  
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String)
  password = Column(LargeBinary)

class Author(Base):
  __tablename__ = 'authors'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)

  books = relationship("Book", back_populates="author")

class Book(Base):
  __tablename__ = 'books'

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String)
  pages = Column(BigInteger)
  author_id = Column(Integer, ForeignKey("authors.id"))

  author = relationship("Author", back_populates="books")
