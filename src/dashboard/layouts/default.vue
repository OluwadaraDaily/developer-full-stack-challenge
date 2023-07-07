<template>
  <div>
    <Header/>
    <Nuxt/>
  </div>
</template>

<script>
import Header from '../components/Header/Header.vue'
export default {
  components: {
    Header
  },
  data() {
    return {}
  },
  methods: {},
  computed: {
    isUserLoggedIn() {
      return this.$store.getters["getLoggedInState"]
    }
  },
  async mounted() {
    await this.$store.dispatch("refreshToken")
    if (!this.isUserLoggedIn) {
      this.$router.push({ path: '/' })
    }
  }
}
</script>