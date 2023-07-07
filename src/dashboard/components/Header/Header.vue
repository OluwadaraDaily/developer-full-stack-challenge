<template>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>AuthBooks</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse" v-if="isUserLoggedIn"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav v-if="isUserLoggedIn">
      <b-navbar-nav class="mx-auto">
        <b-nav-item to="/authors">
          Authors
        </b-nav-item>
        <b-nav-item to="/books">
          Books
        </b-nav-item>
      </b-navbar-nav>

      <b-navbar-nav class="ml-auto" v-if="isUserLoggedIn">
        <b-button variant="dark" @click="logout">Logout</b-button>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {}
  },
  methods: {
    async logout() {
      await this.$store.dispatch("logout")
      this.$router.push({ path: '/' })
    }
  },
  computed: {
    isUserLoggedIn() {
      return this.$store.getters["getLoggedInState"]
    }
  }
}
</script>

<style lang="scss" scoped>
@import './Header.scss'
</style>