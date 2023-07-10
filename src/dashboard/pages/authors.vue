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
                  data-cy="filter-authors-input"
                ></b-form-input>
    
                <b-input-group-append>
                  <b-button :disabled="!filter" @click="filter = ''">Clear</b-button>
                </b-input-group-append>
              </b-input-group>
            </div>
            <div class="col-5"></div>
            <div class="col-2">
              <b-button v-b-modal.author-modal data-cy="add-author-btn">Add Author</b-button>
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
          tbody-tr-class="author-table-row"
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
        @ok="handleModalOk($event, ['form1'], 'add-author')"
      >
        <b-form ref="form1">
          <b-form-group
            id="input-group-1"
            label="Author's Name"
            label-for="input-1"
            invalid-feedback="Name is required"
            :state="states.form1.state"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Author's Name"
              required
              v-model="authorsName"
              :state="states.form1.state"
              data-cy="author-name-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
      </b-modal>

      <!-- Edit Author Modal -->
      <b-modal 
        id="edit-modal"
        title="Edit Author"
        @hidden="resetEditModal"
        @ok="handleModalOk($event, ['form2'], 'edit-author')"
      >
        <b-form ref="form2">
          <b-form-group
            label="Author's Name"
            label-for="input-1"
            invalid-feedback="Name is required"
            :state="states.form2.state"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Author's Name"
              required
              v-model="currentAuthorData.name"
              :state="states.form2.state"
              data-cy="edit-author-name-input"
            ></b-form-input>
          </b-form-group>
        </b-form>

        <!-- Add Book Form -->
        <hr/>
        <b-row>
          <b-col class="ml-auto">
            <b-button class="mt-2" @click="openAddBookModal" data-cy="add-book-btn">Add Book</b-button>
          </b-col>
        </b-row>

        <!-- Author's Books Table -->
        <b-table
          striped
          hover
          :items="currentAuthorData.books"
          :fields="editAuthorBooksFields"
          class="mt-2"
          @row-clicked="bookRowClicked"
          tbody-tr-class="author-books-table-row"
        >
        </b-table>
      </b-modal>

      <!-- Edit Book Modal -->
      <b-modal 
        id="edit-book-modal"
        title="Edit Book"
        @hidden="resetEditBookModal"
        @ok="handleModalOk($event, ['form5'], 'edit-book')"
      >
        <b-form ref="form5">
          <b-form-group
            id="input-group-1"
            label="Book Name"
            label-for="input-1"
            invalid-feedback="Book Name is required"
            :state="states.form5.state"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Book Name"
              class="mb-2"
              required
              v-model="currentBook.name"
              :state="states.form5.state"
              data-cy="book-name-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form6">
          <b-form-group
            label="Number of Pages"
            label-for="input-1"
            invalid-feedback="Number of pages is required"
            :state="states.form6.state"
          >
            <b-form-input
              id="input-1"
              type="number"
              placeholder="Pages"
              class="mb-2"
              required
              v-model="currentBook.pages"
              :state="states.form6.state"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-button variant="danger" @click="deleteCurrentBook">Delete</b-button>
      </b-modal>

      <!-- Add Author Book Modal -->
      <b-modal 
        id="add-author-book-modal"
        title="Add Book"
        @hidden="resetAddAuthorBookModal"
        @ok="handleModalOk($event, ['form3', 'form4'], 'add-book')"
      >
        <div class="row">
          <div class="col-8">
            <b-form ref="form3">
              <b-form-group
                label="Book name"
                invalid-feedback="Book name is required"
                :state="states.form3.state"
              >
                <b-form-input
                  type="text"
                  placeholder="Book Name"
                  required
                  invalid-feedback="Book name is required"
                  v-model="book.name"
                  :state="states.form3.state"
                  data-cy="add-book-name-input"
                ></b-form-input>
              </b-form-group>
            </b-form>
          </div>
          <div class="col-4">
            <b-form ref="form4">
              <b-form-group
                label="Pages"
                invalid-feedback="Number of pages is required"
                :state="states.form4.state"
              >
                <b-form-input
                  type="number"
                  placeholder="Pages"
                  required
                  v-model="book.pages"
                  :state="states.form4.state"
                  data-cy="add-page-number-input"
                ></b-form-input>
              </b-form-group>
            </b-form>
          </div>
        </div>
      </b-modal>
    </div>
  </div>
</template>

<script>
import api from '../helpers/api'
import { mapGetters } from 'vuex'

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
      currentBookState: null,
      states: {
        form1: {
          state: null
        },
        form2: {
          state: null
        },
        form3: {
          state: null
        },
        form4: {
          state: null
        },
        form5: {
          state: null
        },
        form6: {
          state: null
        }
      }
    }
  },
  methods: {
    checkFormValidity(refTags) {
      let validity = true
      for (const refTag of refTags) {
        const valid = this.$refs[`${refTag}`].checkValidity()
        this.states[`${refTag}`].state = valid
        validity = validity && valid
      }
      return validity
    },
    
    resetModal() {
      this.authorsName = ''
      this.states.form1.state = null
    },
    resetEditModal() {
      this.currentAuthor = {}
      this.states.form2.state = null
    },
    async resetEditBookModal() {
      this.states.form5.state = null
      this.currentBook = {}
      await this.$store.dispatch("authors/getCurrentAuthor", this.currentAuthor.id)
      this.$bvModal.show('edit-modal')
    },
    async resetAddAuthorBookModal() {
      this.book = {
        name: '',
        pages: 0
      }
      this.states.form3.state = null
      this.states.form4.state = null
      await this.$store.dispatch("authors/getCurrentAuthor", this.currentAuthor.id)
      this.$bvModal.show("edit-modal")
    },

    async handleModalOk(event, refTags, type) {
      // Prevent modal from closing & trigger submit handler
      event.preventDefault()
      if (!this.checkFormValidity(refTags)) {
        return
      }
      switch (type) {
        case 'add-author':
          await this.handleAddAuthorSubmit(refTags)
          return;

        case 'edit-author':
          await this.handleEditAuthorSubmit(refTags)
          return;

        case 'edit-book':
          await this.handleBookEditSubmit(refTags)
          return;

        case 'add-book':
          await this.handleAddAuthorBookSubmit(refTags)
          return;

        default:
          return; 
      }
    },

    async handleAddAuthorSubmit(refTags) {
      if (!this.checkFormValidity(refTags)) {
        return
      }
      // Create new Author
      const payload = {
        name: this.authorsName
      }
      await this.$store.dispatch("authors/createAuthor", payload)
      this.$bvModal.hide('author-modal')
    },
    async handleEditAuthorSubmit(refTags) {
      if (!this.checkFormValidity(refTags)) {
        return
      }
      // Update Author
      const payload = {
        id: this.currentAuthorData.id,
        name: this.currentAuthorData.name
      }
      await this.$store.dispatch("authors/updateAuthor", payload)
      this.$bvModal.hide('edit-modal')
    },
    async handleBookEditSubmit(refTags) {
      if (!this.checkFormValidity(refTags)) {
        return
      }
      // Update Book
      const payload = {
        authorId: this.currentAuthorData.id,
        bookId: this.currentBook.id,
        name: this.currentBook.name,
        pages: this.currentBook.pages
      }
      await this.$store.dispatch("authors/updateBook", payload)

      this.$bvModal.hide('edit-book-modal')
    },
    async handleAddAuthorBookSubmit(refTags) {
      if (!this.checkFormValidity(refTags)) {
        return
      }
      const payload = {
        id: this.currentAuthorData.id,
        ...this.book
      }
      await this.$store.dispatch("authors/createBook", payload)
      this.$bvModal.hide('add-author-book-modal')
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
      this.$bvModal.hide('edit-modal')
    },
    openAddBookModal() {
      this.$bvModal.show("add-author-book-modal")
      this.$bvModal.hide("edit-modal")
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
    if (!allAuthorsResponse.isSuccess) {
      this.fetchError = allAuthorsResponse.message
      $fetchState.error = true
    }
  }
}
</script>