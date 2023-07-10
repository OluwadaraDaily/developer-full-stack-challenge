import * as appMocks from "../support/mocks/app";

describe("Books Tests", () => {
  beforeEach(() => {
    cy.login()
    cy.get("[data-cy='books-nav-link']").click()
  })

  it('should display error without fetching books data', () => {
    cy.contains("An error occurred :(")
  })

  it.only('should add a book', () => {
    cy.fixture("app/books.json").then((res) => {
      appMocks.fetchBooks(res.successfullyFetchedBooks)
    })
    
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
    })

    cy.wait('@fetchBooks')
    cy.wait('@fetchAuthors')
  })
})