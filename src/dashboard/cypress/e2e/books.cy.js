import * as appMocks from "../support/mocks/app";

describe("Books Tests", () => {
  beforeEach(() => {
    cy.login()
    cy.get("[data-cy='books-nav-link']").click()
  })

  it('should display error without fetching books data', () => {
    cy.contains("An error occurred :(")
  })

  it('should add a book', () => {
    cy.fixture("app/books.json").then((res) => {
      appMocks.fetchBooks(res.successfullyFetchedBooks)
      appMocks.addBook(res.successfullyAddedBook)
    })
    
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })

    cy.get("[data-cy='add-book-btn']").click()

    cy.get("button.btn-primary").first().click()

    cy.contains("Book name is required").should('be.visible')
    cy.contains("Number of pages is required").should('be.visible')
    cy.contains("Author is required").should('be.visible')

    cy.get("[data-cy='add-book-name-input']").type("The Philosopher's Stone")
    cy.get("[data-cy='add-number-of-pages-input']").type("234")

    cy.get("[data-cy='add-authors-dropdown']").click()

    cy.get(".vue-treeselect__menu-container").children().first().click()

    cy.get("button.btn-primary").first().click()

    cy.wait('@fetchBooks')
    cy.wait('@addBook')
    cy.wait('@fetchAuthors')
  })

  it('should filter books', () => {
    cy.fixture("app/books.json").then((res) => {
      appMocks.fetchBooks(res.successfullyFetchedBooks)
    })
    
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })

    cy.get("[data-cy='filter-search-input']").clear()
    cy.get("[data-cy='filter-search-input']").type('economic')

    cy.contains("Economic store.").should('be.visible')
    cy.contains("Key economic.").should('be.visible')

    cy.get("[data-cy='clear-filter-btn']").click()

    cy.get("[data-cy='clear-filter-btn']").should('be.disabled')

    cy.wait('@fetchBooks')
    cy.wait('@fetchAuthors')
  })

  it('should edit book', () => {
    cy.fixture("app/books.json").then((res) => {
      appMocks.fetchBooks(res.successfullyFetchedBooks)
      appMocks.updateBook(res.successfullyUpdatedBook)
    })
    
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })

    cy.get(".books-table-row").first().click()

    cy.get("[data-cy='add-book-name-input']").clear()

    cy.get("button.btn-primary").first().click()
    cy.contains("Book name is required").should('be.visible')

    cy.get("[data-cy='add-book-name-input']").type("Interesting piece")

    cy.get("[data-cy='add-number-of-pages-input']").clear()

    cy.get("button.btn-primary").first().click()
    cy.contains("Number of pages is required").should('be.visible')

    cy.get("[data-cy='add-number-of-pages-input']").type("150")

    cy.get("button.btn-primary").first().click()

    cy.wait('@fetchBooks')
    cy.wait('@updateBook')
    cy.wait('@fetchAuthors')
  })
})