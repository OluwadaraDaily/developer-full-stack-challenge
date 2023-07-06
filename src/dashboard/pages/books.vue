<template>
  <div>
    <p v-if="$fetchState.pending">Fetching books...</p>
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
              <b-button v-b-modal.add-book-modal>Add Book</b-button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-10 mt-3 mx-auto">
        <b-table
          striped
          hover 
          :items="booksList"
          :fields="fields"
          :filter="filter"
          :per-page="perPage"
          :current-page="currentPage"
          @row-clicked="rowClicked"
          bordered
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
        <b-form @submit.prevent="handleSubmit" ref="form1">
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
        <b-form @submit.prevent="handleSubmit" ref="form4">
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
      fields: [
        { key: 'id', thClass: 'd-none', tdClass: 'd-none' },
        { key: 'name' },
        { key: 'author' },
        { key: 'number_of_pages' },
        { key: 'author_id', thClass: 'd-none', tdClass: 'd-none' }
      ],
      books: [],
      authors: [],
      authorOptions: [],
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
      console.log('Item ->', item)
      console.log('Index ->', index)
      console.log('Event ->', event)
      // const authorId = item.id
      // const authorResponse = await api.getAuthor(authorId)
      // this.currentAuthor = authorResponse.data
      this.currentBookData = item
      console.log('currentBookData ->', this.currentBookData)
      // Open Modal
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
      // this.currentBookData = {}
    },
    async handleAddBookModalOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      await this.handleAddBookSubmit()
    },
    async handleEditBookModalOk(bvModalEvent) {
      // Prevent modal from closing
      bvModalEvent.preventDefault()
      // Trigger submit handler
      await this.handleEditBookSubmit()
    },
    async handleAddBookSubmit() {
      // Exit when the form isn't valid
      if (!this.checkAddBookFormValidity()) {
        return
      }
      // Create new Book
      const payload = {...this.book }
      if (!!this.author) {
        console.log('Author ->', this.author)
        await api.createBook(this.author, payload)
        // Hide the modal
        this.$bvModal.hide('add-book-modal')
      }
    },
    async handleEditBookSubmit() {
      // Exit when the form isn't valid
      if (!this.checkEditBookFormValidity()) {
        return
      }
      // Update Book
      const payload = {
        name: this.currentBookData.name,
        pages: this.currentBookData.number_of_pages
      }
      console.log('Payload ->', payload)
      console.log('Author ID ->', this.currentBookData.author_id)
      console.log('BOOK ID ->', this.currentBookData.id)
      await api.updateBook(this.currentBookData.author_id, this.currentBookData.id, payload)
      // Hide the modal
      this.$bvModal.hide('edit-book-modal')
    }
  },
  computed: {
    booksList() {
      return this.books.map((book) => ({
        id: book.id,
        name: book.name,
        author: this.authors.find(author => author.id === book.author_id).name,
        number_of_pages: book.pages,
        author_id: this.authors.find(author => author.id === book.author_id).id,
      }))
    },
    rows() {
      return this.books.length
    }
  },
  async fetch() {
    const booksResponse = await api.fetchBooks()
    const authorsResponse = await api.fetchAuthors()
    console.log('Response 1 ->', booksResponse)
    console.log('Response 2 ->', authorsResponse)
    if (booksResponse.status === 200 && authorsResponse.status === 200) {
      this.books = booksResponse.data
      this.authors = authorsResponse.data
      this.authorOptions = authorsResponse.data.map((item) => ({
        id: item.id,
        label: item.name
      }))
    } else {
      $fetchState.error = true
    }
  }
}
</script>