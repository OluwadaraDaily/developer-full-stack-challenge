<template>
  <b-card class="col-6 mt-5 mx-auto">
    <b-form @submit.prevent="submitLoginForm">
      <b-form-group
        id="input-group-1"
        label="Username"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          type="text"
          placeholder="Username"
          required
          v-model="form.username"
          data-cy="username-input"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        label="Password"
        label-for="input-1"
        description="Ensure it is secret..."
        data-cy="password-input"
      >
        <b-form-input
          id="input-2"
          type="password"
          placeholder="********"
          required
          v-model="form.password"
        ></b-form-input>
      </b-form-group>
      <b-row>
        <b-col align-self="end">
          <b-button variant="outline-primary" type="submit" data-cy="submit-login">Login</b-button>
        </b-col>
      </b-row>
    </b-form>
  </b-card>
</template>

<script>
export default {
  name: 'Login',
  components: {},
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      baseUrl: process.env.NUXT_ENV_API_URL,
      errorText: '',
      showError: false
    }
  },
  methods: {
    async submitLoginForm() {
      let formData = new FormData()
      formData.append('username', this.form.username)
      formData.append('password', this.form.password)

      const loginResponse = await this.$store.dispatch("login", formData)
      if (loginResponse.isSuccess) {
        this.$router.push({ path: '/authors' })
      }
    }
  },
  computed: {
    isUserLoggedIn() {
      return this.$store.state.isLoggedIn
    }
  },
  async mounted() {
    // If logged in, push to authors page
    if (this.isUserLoggedIn) {
      this.$router.push({ path: '/authors' })
    }
  }
}
</script>