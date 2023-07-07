import api from '../helpers/api'

export const state = () => ({
  allAuthors: [],
  currentAuthor: {},
  currentAuthorBooks: []
})

export const getters = {
  getAllAuthors(state) {
    return state.allAuthors
  },
  getCurrentAuthor(state) {
    return state.currentAuthor
  },
  getAllCurrentAuthorBooks(state) {
    return state.currentAuthorBooks
  }
}

export const mutations = {
  SET_ALL_AUTHORS(state, data) {
    state.allAuthors = [...data]
  },
  SET_CURRENT_AUTHOR(state, data) {
    state.currentAuthor = data
  },
  SET_ALL_AUTHOR_BOOKS(state, data) {
    state.currentAuthorBooks = [...data]
  }
}

export const actions = {
  async fetchAllAuthors({ commit }) {
    try {
      const response = await api.fetchAuthors()
      commit('SET_ALL_AUTHORS', response.data)
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async createAuthor({ dispatch }, payload) {
    try {
      const response = await api.createAuthor(payload)
      dispatch('fetchAllAuthors')
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async updateAuthor({ dispatch }, payload) {
    try {
      const authorId = payload.id
      delete payload.id
      const response = await api.updateAuthor(authorId, payload)
      dispatch('fetchAllAuthors')
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async getCurrentAuthor({ commit }, id) {
    try {
      const response = await api.getAuthor(id)
      commit('SET_CURRENT_AUTHOR', response.data)
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async fetchAllAuthorBooks({ commit }) {
    try {
      const response = await api.fetchAuthorBooks()
      commit('SET_ALL_AUTHOR_BOOKS', response.data)
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async createBook({ commit, dispatch }, payload) {
    try {
      const authorId = payload.id
      delete payload.id

      const response = await api.createBook(authorId, payload)
      dispatch('getCurrentAuthor', authorId)
      dispatch('fetchAllAuthors')
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
      dispatch('getCurrentAuthor', authorId)
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async deleteBook({ dispatch }, payload) {
    try {
      const { authorId, bookId } = payload

      const response = await api.deleteBook(authorId, bookId)
      dispatch('getCurrentAuthor', authorId)
      dispatch('fetchAllAuthors')
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  }
}