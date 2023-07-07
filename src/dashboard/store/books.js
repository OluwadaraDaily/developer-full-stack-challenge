import api from '../helpers/api'

export const state = () => ({
  booksList: []
})

export const getters = {
  getBooksList(state) {
    return state.booksList
  }
}

export const mutations = {
  SET_BOOKS_LIST(state, data) {
    state.booksList = [...data]
  }
}

export const actions = {
  async fetchBooks({ commit }) {
    try {
      const { data: books } = await api.fetchBooks()
      const { data: authors } = await api.fetchAuthors()
      const booksList = books.map((book) => ({
        id: book.id,
        name: book.name,
        author: authors.find(author => author.id === book.author_id).name,
        number_of_pages: book.pages,
        author_id: authors.find(author => author.id === book.author_id).id,
      }))
      commit('SET_BOOKS_LIST', booksList)
      return { data: booksList, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async createBook({ dispatch }, payload) {
    try {
      const { authorId } = payload
      delete payload.authorId

      const response = await api.createBook(authorId, payload)
      dispatch('fetchBooks')
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async updateBook({ dispatch }, payload) {
    try {
      const { authorId, bookId } = payload
      delete payload.authorId
      delete payload.bookId

      const response = await api.updateBook(authorId, bookId, payload)
      dispatch('fetchBooks')
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  }
}