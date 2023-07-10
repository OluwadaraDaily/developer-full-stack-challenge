import * as appMocks from "../support/mocks/app";

describe('Authors Tests', () => {
  beforeEach(() => {
    cy.login()
  })
  it('should add an author', () => {
    cy.fixture("app/authors.json").then((res) => {
      appMocks.createAuthor(res.successfullyAddedAuthor)
    })
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })
    cy.get("[data-cy='add-author-btn']").click()
    cy.get("button.btn-primary").click()
    cy.get("#author-modal").contains('Name is required').should('be.visible')
    cy.get("[data-cy='author-name-input']").type("Chinua Achebe")
    cy.get("button.btn-primary").click()

    cy.wait('@createAuthor')
    cy.wait('@fetchAuthors')
  })

  it('should filter authors', () => {
    cy.get("[data-cy='filter-authors-input']").type("Author")
    cy.contains("New Author 1").should('be.visible')
    cy.get("[data-cy='filter-authors-input']").clear()
  })

  it('should to edit an author', () => {
    cy.fixture("app/authors.json").then((res) => {
      appMocks.getAuthor(res.retrieveAuthorSuccessfully)
      appMocks.updateAuthor(res.successfullyUpdateAuthor)
    })
    cy.get(".author-table-row").first().click()
    cy.get("[data-cy='edit-author-name-input']").clear()
    cy.get("button.btn-primary").click()
    cy.get("[data-cy='edit-author-name-input']").scrollIntoView()
    cy.contains('Name is required').should('be.visible')
    cy.get("[data-cy='edit-author-name-input']").type("Chimamanda Adichie")
    cy.get("button.btn-primary").click()
    cy.wait('@getAuthor')
    cy.wait('@updateAuthor')
  })

  it('should add a book to an author', () => {
    cy.fixture("app/authors.json").then((res) => {
      appMocks.getAuthor(res.retrieveAuthorSuccessfully)
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })

    cy.fixture("app/books.json").then((res) => {
      appMocks.addBook(res.successfullyAddedBook)
    })

    cy.get(".author-table-row").first().click()
    cy.get("[data-cy='add-book-btn']").click()

    cy.get("button.btn-primary").first().click()

    cy.contains('Book name is required')

    cy.get("[data-cy='add-book-name-input']").type("Harry Potter")

    cy.get("[data-cy='add-page-number-input']").clear()

    cy.get("button.btn-primary").first().click()

    cy.contains("Number of pages is required")

    cy.get("[data-cy='add-page-number-input']").type("148")

    cy.get("button.btn-primary").first().click()

    cy.wait('@getAuthor')
    cy.wait('@fetchAuthors')
    cy.wait('@addBook')
  })

  it("should edit an author's book", () => {
    cy.fixture("app/authors.json").then((res) => {
      appMocks.getAuthor(res.retrieveAuthorSuccessfully)
    })

    cy.fixture("app/books.json").then((res) => {
      appMocks.getBook(res.retrievedBookSuccessfully)
      appMocks.updateBook(res.successfullyUpdatedBook)
    })

    cy.get(".author-table-row").first().click()
    cy.get(".author-books-table-row").first().click()
    cy.get("[data-cy='book-name-input']").clear()
    cy.get("button.btn-primary").first().click()
    cy.get("[data-cy='book-name-input']").scrollIntoView()
    cy.contains('Book Name is required').should('be.visible')
    cy.get("[data-cy='book-name-input']").type("A New Book, I suppose.")
    cy.get("button.btn-primary").first().click()

    cy.wait('@getAuthor')
    cy.wait('@getBook')
    cy.wait('@updateBook')
  })
})