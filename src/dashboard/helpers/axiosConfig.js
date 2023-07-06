import axios from 'axios';

axios.defaults.baseURL = process.env.NUXT_ENV_API_URL;
axios.defaults.headers.post['Content-Type'] = 'application/json';

axios.defaults.headers.common['Authorization'] = `${localStorage.getItem('token')}`;
window.addEventListener('localstorage-changed', (event) => {
  axios.defaults.headers.common['Authorization'] = `${event.detail.token}`;
});

export { axios };
