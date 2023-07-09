import { axios } from './axiosConfig';

async function login(payload) {
  axios.defaults.headers.post["Content-Type"] = "multipart/form-data"
  const response = await axios.post("/token", payload)
  return response;
}

async function getToken() {

}

async function verifyToken() {

}

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

export default {
  fetchAuthors,
  fetchBooks,
  createAuthor,
  getAuthor,
  updateAuthor,
  createBook,
  updateBook,
  getBook,
  deleteBook,
  login
}