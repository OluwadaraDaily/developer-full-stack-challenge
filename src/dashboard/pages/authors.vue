<template>
  <div>
    <p v-if="$fetchState.pending">Fetching authors...</p>
    <p v-else-if="$fetchState.error">An error occurred :(</p>
    <div v-else>
      <div class="row mt-5">
        <div class="col-10 mx-auto">
          <div class="row">
            <div class="col-5">
              <b-input-group size="sm">
                <b-form-input
                  id="filter-input"
                  v-model="filter"
                  type="search"
                  placeholder="Type to Search"
                ></b-form-input>
    
                <b-input-group-append>
                  <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                </b-input-group-append>
              </b-input-group>
            </div>
            <div class="col-5"></div>
            <div class="col-2">
              <b-button v-b-modal.author-modal>Add Author</b-button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-10 mt-3 mx-auto">
        <b-table
          striped
          hover 
          :items="authorsList"
          :fields="fields"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          @row-clicked="rowClicked"
          bordered
        ></b-table>
        <div class="row ml-auto">
          <div class="ml-auto">
            <b-pagination
              v-model="currentPage"
              :total-rows="rows"
              :per-page="perPage"
              aria-controls="my-table"
            ></b-pagination>
          </div>
        </div>
      </div>

      <!-- Modals -->
      <!-- Add Author Modal -->
      <b-modal 
        id="author-modal"
        title="Add Author"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleOk"
      >
        <b-form @submit.prevent="handleSubmit" ref="form1">
          <b-form-group
            id="input-group-1"
            label="Author's Name"
            label-for="input-1"
            invalid-feedback="Name is required"
            :state="authorsNameState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Author's Name"
              required
              v-model="authorsName"
              :state="authorsNameState"
            ></b-form-input>
          </b-form-group>
          <b-row>
            <b-col align-self="end">
              <b-button variant="outline-primary" type="submit">Add Author</b-button>
            </b-col>
          </b-row>
        </b-form>
      </b-modal>

      <!-- Edit Author Modal -->
      <b-modal 
        id="edit-modal"
        title="Edit Author"
        @hidden="resetModal"
        @ok="handleEditOk"
      >
        <b-form @submit.prevent="handleSubmit" ref="form2">
          <b-form-group
            id="input-group-1"
            label="Author's Name"
            label-for="input-1"
            invalid-feedback="Name is required"
            :state="authorsNameState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Author's Name"
              required
              v-model="currentAuthor.name"
              :state="currentAuthorState"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form3">
          <b-form-group>
            <div class="row">
              <div class="col-8">
                <b-form-input
                  type="text"
                  placeholder="Book Name"
                  required
                  v-model="book.name"
                  :state="bookNameState"
                ></b-form-input>
              </div>
              <div class="col-4">
                <b-form-input
                  type="number"
                  placeholder="Pages"
                  required
                  v-model="book.pages"
                ></b-form-input>
              </div>
            </div>
            <b-button class="mt-2" @click="createBook">Add Book</b-button>
          </b-form-group>
        </b-form>
        <b-table
          striped
          hover
          :items="currentAuthor.books"
          :fields="editAuthorBooksFields"
          class="mt-2"
          @row-clicked="bookRowClicked"
        >
        <template #cell(delete)>
          <b-button>Delete</b-button>
        </template>
        </b-table>
      </b-modal>

      <!-- Edit Book Modal -->
      <b-modal 
        id="edit-book-modal"
        title="Edit Author"
        @hidden="resetModal"
        @ok="handleBookEditOk"
      >
        <b-form ref="form4">
          <b-form-group
            id="input-group-1"
            label="Book Name"
            label-for="input-1"
            invalid-feedback="Book Name is required"
            :state="bookNameState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Book Name"
              class="mb-2"
              required
              v-model="currentBook.name"
              :state="currentBookState"
            ></b-form-input>

            <b-form-input
              id="input-1"
              type="number"
              placeholder="Pages"
              class="mb-2"
              required
              v-model="currentBook.pages"
              :state="currentBookState"
            ></b-form-input>
          </b-form-group>
          <b-button variant="danger" @click="deleteCurrentBook">Delete</b-button>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import api from '../helpers/api'
export default {
  name: 'Authors',
  data() {
    return {
      items: [],
      fields: [
        { key: 'id', label: 'ID', thClass: 'd-none', tdClass: 'd-none' },
        { key: 'name', label: 'Name' },
        { key: 'number_of_books', label: 'Number of Books' }
      ],
      perPage: 10,
      currentPage: 1,
      editAuthorBooksFields: [
        { key: 'name', label: 'Name' },
        { key: 'pages', label: 'Number of Pages' }
      ],
      filter: '',
      authorsName: '',
      authorsNameState: null,
      currentAuthor: {},
      currentAuthorState: null,
      book: {
        name: '',
        pages: 0
      },
      bookNameState: null,
      currentBook: {},
      currentBookState: null
    }
  },
  methods: {
    checkFormValidity() {
      const valid = this.$refs.form1.checkValidity()
      this.authorsNameState = valid
      return valid
    },
    checkEditFormValidity() {
      const valid = this.$refs.form2.checkValidity()
      this.currentAuthorState = valid
      return valid
    },
    checkBookFormValidity() {
      const valid = this.$refs.form3.checkValidity()
      this.bookNameState = valid
      return valid
    },
    checkEditBookFormValidity() {
      const valid = this.$refs.form4.checkValidity()
      this.currentBookState = valid
      return valid
    },
    resetModal() {
      this.authorsName = ''
      this.authorsNameState = null
    },
    async handleOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      await this.handleSubmit()
    },
    handleEditOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      this.handleEditSubmit()
    },
    handleBookEditOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      this.handleBookEditSubmit()
    },
    async handleSubmit() {
      // Exit when the form isn't valid
      if (!this.checkFormValidity()) {
        return
      }
      // Create new Author
      const payload = {
        name: this.authorsName
      }
      await api.createAuthor(payload)
      // Hide the modal
      this.$bvModal.hide('author-modal')
    },
    async handleEditSubmit() {
      // Exit when the form isn't valid
      if (!this.checkEditFormValidity()) {
        return
      }
      // Update Author
      const payload = {
        name: this.currentAuthor.name
      }
      await api.updateAuthor(this.currentAuthor.id, payload)
      this.$bvModal.hide('edit-modal')
    },
    async handleBookEditSubmit() {
      // Exit when the form isn't valid
      if (!this.checkEditBookFormValidity()) {
        return
      }
      // Update Book
      const payload = {
        name: this.currentBook.name,
        pages: this.currentBook.pages
      }
      await api.updateBook(this.currentAuthor.id, this.currentBook.id, payload)
      this.$bvModal.hide('edit-book-modal')
    },
    async deleteCurrentBook() {
      await api.deleteBook(this.currentAuthor.id, this.currentBook.id)
      this.$bvModal.hide('edit-book-modal')
    },
    async rowClicked(item, index, event) {
      const authorId = item.id
      const authorResponse = await api.getAuthor(authorId)
      this.currentAuthor = authorResponse.data

      // Open Modal
      this.$bvModal.show('edit-modal')
    },
    async bookRowClicked(item, index, event) {
      const bookId = item.id
      const bookResponse = await api.getBook(bookId)
      this.currentBook = bookResponse.data

      this.$bvModal.show('edit-book-modal')
    },
    async createBook() {
      // Exit when the form isn't valid
      if (!this.checkBookFormValidity()) {
        return
      }
      await api.createBook(this.currentAuthor.id, this.book)
      this.book = {
        name: '',
        pages: 0
      }
    },
    async openEditBookModal() {
      this.$bvModal.show('edit-book-modal')
    }
  },
  computed: {
    authorsList() {
      return this.items.map((author) => ({
        id: author.id,
        name: author.name,
        number_of_books: author.books.length
      }))
    },
    rows() {
      return this.items.length
    }
  },
  async fetch() {
    const response = await api.fetchAuthors()
    console.log('Response ->', response)
    if (response.status === 200) {
      this.items = response.data
    } else {
      $fetchState.error = true
    }
  }
}
</script>