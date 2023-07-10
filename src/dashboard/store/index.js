import api from '../helpers/api'

import { axios } from '../helpers/axiosConfig';

export const state = () => ({
  token: '',
  isLoggedIn: false
})

export const getters = {
  getToken(state) {
    return state.token
  },
  getLoggedInState(state) {
    return state.isLoggedIn
  }
}

export const mutations = {
  SET_TOKEN(state, data) {
    state.token = `Bearer ${data}`
    state.isLoggedIn = true
  },
  RESET_TOKEN(state) {
    localStorage.removeItem('token')
    state.token = ''
    state.isLoggedIn = false
  }
}

export const actions = {
  async login({ commit }, payload) {
    try {
      const response = await api.login(payload)
      console.log('LOGIN API RESPONSE ->', response)
      if (response.data.access_token) {
        localStorage.setItem('token', `Bearer ${response.data.access_token}`)
        axios.defaults.headers.common['Authorization'] = `${localStorage.getItem('token')}`;
        commit('SET_TOKEN', `${response.data.token_type} ${response.data.access_token}`)
      }
      return { data: response.data, isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },
  async logout({ commit }) {
    try {
      commit('RESET_TOKEN')
      return { data: [], isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  },

  async refreshToken({ commit }) {
    try {
      const token = localStorage.getItem("token")
      if (token !== null || !!token) {
        commit('SET_TOKEN', token)
        return { data: [], isSuccess: true }
      }
      commit('RESET_TOKEN')
    } catch (error) {
      return { isSuccess: false, message: error.message };
    }
  }
}

export const strict = false