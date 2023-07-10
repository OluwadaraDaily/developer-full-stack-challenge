<template>
  <div>
    <p v-if="$fetchState.pending">Fetching books...</p>
    <p v-else-if="$fetchState.error">An error occurred :(</p>
    <div v-else>
      <!-- Top Section -->
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
                  data-cy="filter-search-input"
                ></b-form-input>
    
                <b-input-group-append>
                  <b-button :disabled="!filter" @click="filter = ''" data-cy="clear-filter-btn">Clear</b-button>
                </b-input-group-append>
              </b-input-group>
            </div>
            <div class="col-5"></div>
            <div class="col-2">
              <b-button v-b-modal.add-book-modal data-cy="add-book-btn">Add Book</b-button>
            </div>
          </div>
        </div>
      </div>

      <!-- Books Table -->
      <div class="col-10 mt-3 mx-auto">
        <b-table
          striped
          responsive
          hover 
          :items="booksList"
          :fields="fields"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          @row-clicked="rowClicked"
          bordered
          tbody-tr-class="books-table-row"
        >
        </b-table>
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
      <!-- Add Book Modal -->
      <b-modal 
        id="add-book-modal"
        title="Add Book"
        @show="resetModal"
        @hidden="resetModal"
        @ok="handleAddBookModalOk"
      >
        <b-form ref="form1">
          <b-form-group
            id="input-group-1"
            label="Book Name"
            label-for="input-1"
            invalid-feedback="Book name is required"
            :state="bookState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Book Name"
              required
              v-model="book.name"
              :state="bookState"
              data-cy="add-book-name-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form2">
          <b-form-group
            id="input-group-2"
            label="Number of Pages"
            label-for="input-2"
            invalid-feedback="Number of pages is required"
            :state="numberOfPagesState"
          >
            <b-form-input
              id="input-2"
              type="number"
              placeholder="Pages"
              required
              v-model="book.pages"
              :state="numberOfPagesState"
              data-cy="add-number-of-pages-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form3">
          <b-form-group
            id="input-group-3"
            label="Author"
            label-for="input-2"
            invalid-feedback="Author is required"
            :state="authorState"
          >
            <treeselect
              :multiple="false"
              :options="authorOptions"
              placeholder="Select author..."
              v-model="author"
              required
              data-cy="add-authors-dropdown"
            />
          </b-form-group>
        </b-form>
      </b-modal>

      <!-- Edit Book Modal -->
      <b-modal 
        id="edit-book-modal"
        title="Edit Book"
        @hidden="resetEditModal"
        @ok="handleEditBookModalOk"
      >
        <b-form ref="form4">
          <b-form-group
            id="input-group-1"
            label="Book Name"
            label-for="input-1"
            invalid-feedback="Book name is required"
            :state="editBookState"
          >
            <b-form-input
              id="input-1"
              type="text"
              placeholder="Book Name"
              required
              v-model="currentBookData.name"
              :state="editBookState"
              data-cy="add-book-name-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form5">
          <b-form-group
            id="input-group-2"
            label="Number of Pages"
            label-for="input-2"
            invalid-feedback="Number of pages is required"
            :state="editNumberOfPagesState"
          >
            <b-form-input
              id="input-2"
              type="number"
              placeholder="Pages"
              required
              v-model="currentBookData.number_of_pages"
              :state="editNumberOfPagesState"
              data-cy="add-number-of-pages-input"
            ></b-form-input>
          </b-form-group>
        </b-form>
        <b-form ref="form6">
          <b-form-group
            id="input-group-3"
            label="Author"
            label-for="input-2"
            invalid-feedback="Author is required"
            :state="editAuthorState"
          >
            <treeselect
              :multiple="false"
              :options="authorOptions"
              placeholder="Select author..."
              v-model="currentBookData.author_id"
              required
            />
          </b-form-group>
        </b-form>
      </b-modal>
    </div>
  </div>
</template>

<script>
import api from '../helpers/api'
import Treeselect from '@riophae/vue-treeselect'
import '@riophae/vue-treeselect/dist/vue-treeselect.css'
export default {
  name: 'Books',
  components: {
    Treeselect
  },
  data() {
    return {
      fetchError: "",
      fields: [
        { key: 'id', thClass: 'd-none', tdClass: 'd-none' },
        { key: 'name' },
        { key: 'author' },
        { key: 'number_of_pages' },
        { key: 'author_id', thClass: 'd-none', tdClass: 'd-none' }
      ],
      books: [],
      authors: [],
      filter: '',
      perPage: 10,
      currentPage: 1,
      bookState: null,
      book: {
        name: '',
        pages: 0
      },
      numberOfPagesState: null,
      author: null,
      authorState: null,
      currentBookData: {},
      editBookState: null,
      editNumberOfPagesState: null,
      editAuthorState: null
    }
  },
  methods: {
    checkAddBookFormValidity() {
      const validForm1 = this.$refs.form1.checkValidity()
      const validForm2 = this.$refs.form2.checkValidity()
      const validForm3 = this.$refs.form3.checkValidity()

      this.bookState = validForm1
      this.numberOfPagesState = validForm2
      this.authorState = validForm3

      return validForm1 && validForm2 && validForm3
    },
    checkEditBookFormValidity() {
      const validForm4 = this.$refs.form4.checkValidity()
      const validForm5 = this.$refs.form5.checkValidity()
      const validForm6 = this.$refs.form6.checkValidity()

      this.editBookState = validForm4
      this.editNumberOfPagesState = validForm5
      this.editAuthorState = validForm6

      return validForm4 && validForm5 && validForm6
    },
    async rowClicked(item, index, event) {
      this.currentBookData = {...item}

      this.$bvModal.show('edit-book-modal')
    },
    resetModal() {
      this.book = {
        name: '',
        page: 0
      }
      this.bookState = null
      this.numberOfPagesState = null
      this.author = null
      this.authorState = null
    },
    resetEditModal() {
      this.currentBookData = {}
      this.editBookState = null
      this.editNumberOfPagesState = null
    },
    async handleAddBookModalOk(bvModalEvent) {
      // Prevent modal from closing & Trigger submit handler
      bvModalEvent.preventDefault()
      await this.handleAddBookSubmit()
    },
    async handleEditBookModalOk(bvModalEvent) {
      // Prevent modal from closing & Trigger submit handler
      bvModalEvent.preventDefault()
      await this.handleEditBookSubmit()
    },
    async handleAddBookSubmit() {
      if (!this.checkAddBookFormValidity()) {
        return
      }
      // Create new Book
      const payload = {
        authorId: this.author,
        ...this.book
      }
      await this.$store.dispatch("books/createBook", payload)

      this.$bvModal.hide('add-book-modal')
    },
    async handleEditBookSubmit() {
      if (!this.checkEditBookFormValidity()) {
        return
      }
      // Update Book
      const payload = {
        authorId: this.currentBookData.author_id,
        bookId: this.currentBookData.id,
        name: this.currentBookData.name,
        pages: this.currentBookData.number_of_pages
      }
      await this.$store.dispatch("books/updateBook", payload)

      this.$bvModal.hide('edit-book-modal')
    }
  },
  computed: {
    booksList() {
      return this.$store.getters["books/getBooksList"]
    },
    rows() {
      return this.$store.getters["books/getBooksList"].length
    },
    authorOptions() {
      return this.$store.getters["authors/getAllAuthors"].map((author) => ({
        id: author.id,
        label: author.name
      }))
    }
  },
  async mounted() {
    await this.$store.dispatch("authors/fetchAllAuthors")
  },
  async fetch() {
    const booksListResponse = await this.$store.dispatch("books/fetchBooks")
    if (!booksListResponse.isSuccess) {
      this.fetchError = booksListResponse.message
      $fetchState.error = true
    }
  }
}
</script>