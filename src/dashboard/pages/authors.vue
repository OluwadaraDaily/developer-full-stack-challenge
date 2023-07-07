<template>
  <div>
    <p v-if="$fetchState.pending">Fetching authors...</p>
    <p v-else-if="$fetchState.error">An error occurred: {{ fetchError }}</p>
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
        @ok="handleAddAuthorModalOk"
      >
        <b-form ref="form1">
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
        @hidden="resetEditModal"
        @ok="handleEditOk"
      >
        <b-form ref="form2">
          <b-form-group
            label="Author's Name"
            label-for="input-1"
            invalid-feedback="Name is required"
            :state="currentAuthorState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Author's Name"
              required
              v-model="currentAuthorData.name"
              :state="currentAuthorState"
            ></b-form-input>
          </b-form-group>
        </b-form>

        <!-- Add Book Form -->
        <hr/>
        <div class="row">
          <div class="col-8">
            <b-form ref="form3">
              <b-form-group
                label="Book name"
                invalid-feedback="Book name is required"
                :state="bookNameState"
              >
                <b-form-input
                  type="text"
                  placeholder="Book Name"
                  required
                  invalid-feedback="Book name is required"
                  v-model="book.name"
                  :state="bookNameState"
                ></b-form-input>
              </b-form-group>
            </b-form>
              </div>
              <div class="col-4">
                <b-form ref="form4">
                  <b-form-group
                    label="Pages"
                    invalid-feedback="Number of pages is required"
                    :state="numberOfPagesState"
                  >
                    <b-form-input
                      type="number"
                      placeholder="Pages"
                      required
                      v-model="book.pages"
                      :state="numberOfPagesState"
                    ></b-form-input>
                  </b-form-group>
                </b-form>
              </div>
        </div>
        <b-button class="mt-2" @click="createBook">Add Book</b-button>

        <!-- Author's Books Table -->
        <b-table
          striped
          hover
          :items="currentAuthorData.books"
          :fields="editAuthorBooksFields"
          class="mt-2"
          @row-clicked="bookRowClicked"
        >
        </b-table>
      </b-modal>

      <!-- Edit Book Modal -->
      <b-modal 
        id="edit-book-modal"
        title="Edit Book"
        @hidden="resetEditBookModal"
        @ok="handleBookEditOk"
      >
        <b-form ref="form5">
          <b-form-group
            id="input-group-1"
            label="Book Name"
            label-for="input-1"
            invalid-feedback="Book Name is required"
            :state="currentBookState"
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
import { mapMutations, mapGetters } from 'vuex'

export default {
  name: 'Authors',
  data() {
    return {
      fetchError: null,
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
      numberOfPagesState: null,
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
      const validForm3 = this.$refs.form3.checkValidity()
      const validForm4 = this.$refs.form4.checkValidity()
      this.bookNameState = validForm3
      this.numberOfPagesState = validForm4
      return validForm3 && validForm4
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
    resetEditModal() {
      this.currentAuthor = {}
      this.currentAuthorState = null
    },
    resetEditBookModal() {
      this.currentBookState = null
      this.currentBook = {}
    },
    async handleAddAuthorModalOk(bvModalEvent) {
      // Prevent modal from closing & trigger submit handler
      bvModalEvent.preventDefault()
      await this.handleAddAuthorSubmit()
    },
    handleEditOk(bvModalEvent) {
      // Prevent modal from closing & trigger submit handler
      bvModalEvent.preventDefault()
      this.handleEditAuthorSubmit()
    },
    handleBookEditOk(bvModalEvent) {
      // Prevent modal from closing & trigger submit handler
      bvModalEvent.preventDefault()
      this.handleBookEditSubmit()
    },
    async handleAddAuthorSubmit() {
      if (!this.checkFormValidity()) {
        return
      }
      // Create new Author
      const payload = {
        name: this.authorsName
      }
      await this.$store.dispatch("authors/createAuthor", payload)
      this.$bvModal.hide('author-modal')
    },
    async handleEditAuthorSubmit() {
      if (!this.checkEditFormValidity()) {
        return
      }
      // Update Author
      const payload = {
        id: this.currentAuthor.id,
        name: this.currentAuthor.name
      }
      await this.$store.dispatch("authors/updateAuthor", payload)
      this.$bvModal.hide('edit-modal')
    },
    async handleBookEditSubmit() {
      if (!this.checkEditBookFormValidity()) {
        return
      }
      // Update Book
      const payload = {
        authorId: this.currentAuthor.id,
        bookId: this.currentBook.id,
        name: this.currentBook.name,
        pages: this.currentBook.pages
      }
      await this.$store.dispatch("authors/updateBook", payload)

      this.$bvModal.hide('edit-book-modal')
    },
    async deleteCurrentBook() {
      const payload = {
        authorId: this.currentAuthor.id,
        bookId: this.currentBook.id
      }
      await this.$store.dispatch("authors/deleteBook", payload)
      
      this.$bvModal.hide('edit-book-modal')
    },
    async rowClicked(item, index, event) {
      const authorId = item.id
      const currentAuthorResponse = await this.$store.dispatch("authors/getCurrentAuthor", authorId)
      this.currentAuthor = currentAuthorResponse.data
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
      const payload = {
        id: this.currentAuthor.id,
        ...this.book
      }
      this.$store.dispatch("authors/createBook", payload)

      this.book = {
        name: '',
        pages: 0
      }
      this.bookNameState = null
      this.numberOfPagesState = null
    }
  },
  computed: {
    ...mapGetters(["getAllAuthors"]),
    authorsList() {
      return this.$store.getters["authors/getAllAuthors"].map((author) => ({
        id: author.id,
        name: author.name,
        number_of_books: author.books.length
      }))
    },
    currentAuthorData() {
      return this.$store.getters["authors/getCurrentAuthor"]
    },
    rows() {
      return this.$store.getters["authors/getAllAuthors"].length
    }
  },
  async fetch() {
    const allAuthorsResponse = await this.$store.dispatch('authors/fetchAllAuthors')
    // console.log('allAuthorsResponse =>', allAuthorsResponse)
    if (!allAuthorsResponse.isSuccess) {
      this.fetchError = allAuthorsResponse.message
      $fetchState.error = true
    }
  }
}
</script>