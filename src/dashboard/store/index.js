export const state = () => ({
  token: localStorage.getItem('token')
})

export const getters = {
  getToken(state) {
    return state.token
  }
}

export const mutations = {
}

export const actions = {
}

export const strict = false