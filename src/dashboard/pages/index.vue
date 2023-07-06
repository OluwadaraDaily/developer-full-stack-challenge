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
        ></b-form-input>
      </b-form-group>
      <b-form-group
        id="input-group-2"
        label="Password"
        label-for="input-1"
        description="Ensure it is secret..."
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
          <b-button variant="outline-primary" type="submit">Login</b-button>
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
      try {
        let formData = new FormData()
        formData.append('username', this.form.username)
        formData.append('password', this.form.password)
        const options = {
          method: 'POST',
          body: formData
        }
        const response = await fetch(`${this.baseUrl}/token`, options)
          
        if (response.status === 200) {
          console.log('Response OK!')
          console.log('RESPONSE ->', response)
          const data = await response.json()
          console.log('DATA ->', data)
          // Set localStorage with token
          localStorage.setItem('token', `Bearer ${data.access_token}`)

          console.log('LocalStorage =>', localStorage)
          // Login

          this.$router.push({ path: '/authors' })
        } else {
          throw new Error(`${response.status}: ${response.statusText}`)
        }
      } catch (error) {
        // Display error message
        console.log(error.message)
      }
    },
    async isTokenViable() {
      try {
        const options = {
          method: 'GET',
          headers: {
            "Authorization": localStorage.getItem('token')
          }
        }
        const response = await fetch(`${this.baseUrl}/users`, options)
        console.log('Response ->', response)
        if (response.status === 200) {
          return true;
        }
      } catch (error) {
        // Display error message
        console.log(error.message)
      }
    }
  },
  async mounted() {
    // Check if localStorage token is still viable
    const isTokenViable = await this.isTokenViable()
    if (!!isTokenViable) {
      this.$router.push({ path: '/authors' })
    }
  }
}
</script>