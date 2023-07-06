<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>AuthBooks</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse" v-if="tokenAvailable"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav v-if="tokenAvailable">
      <b-navbar-nav class="mx-auto">
        <b-nav-item>
          <NuxtLink to="/authors">Authors</NuxtLink>
        </b-nav-item>
        <b-nav-item>
          <NuxtLink to="/books">Books</NuxtLink>
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto" v-if="tokenAvailable">
        <b-nav-item>
          <b-button variant="dark" @click="logout">Logout</b-button>
        </b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
      tokenAvailable: false
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push({ path: '/' })
    },
    isTokenAvailable() {
      console.log('localStorage.getItem ->', localStorage.getItem('token'))
      if (localStorage.getItem('token') !== null || localStorage.getItem('token')) {
        this.tokenAvailable = true
      } else {
        this.tokenAvailable = false
      }
      console.log('tokenAvailable ->', this.tokenAvailable)
    }
  },
  computed: {
  },
  async mounted() {
    this.isTokenAvailable()
  }
}
</script>

<style lang="scss" scoped>
@import './Header.scss'
</style>