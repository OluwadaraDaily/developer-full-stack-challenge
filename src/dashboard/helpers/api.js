import { axios } from './axiosConfig';

async function fetchAuthors () {
  const response = await axios.get('/authors');
  return response; 
}

async function getAuthor(id) {
  const response = await axios.get(`/authors/${id}`)
  return response;
}

async function updateAuthor(id, payload) {
  const response = await axios.put(`/authors/${id}`, payload)
  return response;
}


async function createAuthor(payload) {
  const response = await axios.post(`/authors`, payload)
  return response
}

async function fetchBooks() {
  const response = await axios.get('/books')
  return response;
}

async function getBook(bookId) {
  const response = await axios.get(`/books/${bookId}`)
  return response;
}

async function createBook(authorId, payload) {
  const response = await axios.post(`/books/authors/${authorId}`, payload)
  return response;
}

async function updateBook(authorId, bookId, payload) {
  const response = await axios.put(`/books/${bookId}/authors/${authorId}`, payload)
  return response;
}

async function deleteBook(authorId, bookId) {
  const response = await axios.delete(`/books/${bookId}/authors/${authorId}`)
  return response;
}

async function isTokenViable() {
  const response = await axios.get(`/users`)
  if (response.status === 200) {
    return true;
  } else {
    return false
  }
}

export default {
  fetchAuthors,
  fetchBooks,
  isTokenViable,
  createAuthor,
  getAuthor,
  updateAuthor,
  createBook,
  updateBook,
  getBook,
  deleteBook
}