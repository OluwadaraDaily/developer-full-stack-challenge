<template>
  <div>
    <Header/>
    <Nuxt/>
  </div>
</template>

<script>
import api from '../helpers/api'
import Header from '../components/Header/Header.vue'
export default {
  components: {
    Header
  },
  data() {
    return {}
  },
  methods: {},
  async mounted() {
    // const isTokenValid = await api.isTokenViable()
    // if (!isTokenValid) {
    //   this.$router.push({ path: '/' })
    // }
  }
}
</script>