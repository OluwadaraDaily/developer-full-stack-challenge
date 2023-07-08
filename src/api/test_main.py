from fastapi.testclient import TestClient

# from .main import app
# from .schemas import *
# from .models import *
from fastapi import Depends
from main import app, get_db
import schemas
import models
import crud
from fastapi.encoders import jsonable_encoder
import json
import time

client = TestClient(app)

context = {}
epoch_time = time.time()

def test_root():
  response = client.get("/")
  context["me"] = "You"
  assert response.status_code == 200
  assert response.json() == {
    "Hello": "World"
  }

def test_create_user():
  username = f"test-user-{epoch_time}"
  payload = {"username": username, "password": "test-password"}
  response = client.post("/users", json=payload)

  context["user"] = {
    "id": response.json().get("id"),
    "username": payload.get("username"),
    "password": payload.get("password")
  }
  assert response.status_code == 200
  assert response.json().get("username") == username

def test_login():
  payload = {
    "username": context["user"].get("username"),
    "password": context["user"].get("password")
  }
  response = client.post("/token", data=payload)

  token_type = response.json().get("token_type")
  token = response.json().get("access_token")
  context["user"]["token"] = f"{token_type} {token}"
  assert response.status_code == 200

def test_create_author_without_token():
  payload = {
    "name": "Oluwadara Daily"
  }
  response = client.post("/authors", json=payload)
  assert response.status_code == 401
  assert response.json().get("detail") == "Not authenticated"

def test_create_author():
  payload = {
    "name": f"Oluwadara Daily-${epoch_time}"
  }
  headers = {
    "Authorization": context["user"].get("token")
  }
  response = client.post("/authors", json=payload, headers=headers)
  context["authors"] = []
  context["authors"].append(response.json())
  books = response.json().get("books")
  assert response.status_code == 200
  assert len(books) == 0

def test_update_author():
  new_author_name = f"Oluwadara Weekly-{epoch_time}"
  author_id = author_id = context["authors"][0].get("id")
  payload = {
    "name": new_author_name
  }
  headers = {
    "Authorization": context["user"].get("token")
  }
  response = client.put(f"/authors/{author_id}", json=payload, headers=headers)
  assert response.status_code == 200
  assert response.json().get("name") == new_author_name

def test_create_book():
  headers = {
    "Authorization": context["user"].get("token")
  }
  book_name = f"Book 1-{epoch_time}"
  payload = {
    "name": book_name,
    "pages": 150
  }
  author_id = context["authors"][0].get("id")
  response = client.post(f"/books/authors/{author_id}", json=payload, headers=headers)
  context["books"] = []
  context["books"].append(response.json())
  assert response.status_code == 200
  assert response.json().get("name") == book_name
  assert response.json().get("pages") == 150

def test_update_book():
  headers = {
    "Authorization": context["user"].get("token")
  }
  new_book_name = f"Book 5-{epoch_time}"
  new_number_of_pages = 200
  payload = {
    "name": new_book_name,
    "pages": new_number_of_pages
  }
  book_id = context["books"][0].get("id")
  author_id = context["books"][0].get("author_id")
  response = client.put(f"/books/{book_id}/authors/{author_id}", json=payload, headers=headers)
  assert response.status_code == 200
  assert response.json().get("name") == new_book_name
  assert response.json().get("pages") == new_number_of_pages


def test_cleanup_db():
  headers = {
    "Authorization": context["user"].get("token")
  }
  authors = context["authors"]
  books = context["books"]
  for book in books:
    book_id = book.get("id")
    author_id = book.get("author_id")
    book_delete_response = client.delete(f"/books/{book_id}/authors/{author_id}", headers=headers)
    assert book_delete_response.json().get("ok") == True

  for author in authors:
    author_id = author.get("id")
    author_delete_response = client.delete(f"/authors/{author_id}", headers=headers)
    assert author_delete_response.json().get("ok") == True

  user_id = context["user"].get("id")
  response = client.delete(f"/users/{user_id}", headers=headers)

  assert response.json().get("ok") == True
