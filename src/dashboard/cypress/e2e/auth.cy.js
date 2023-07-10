import * as authMocks from "../support/mocks/auth";
import * as appMocks from "../support/mocks/app";

describe('Authentication Test', () => {
  it('should log into the app', () => {
    cy.visit("/");
    cy.fixture("auth/login.json").then((res) => {
      authMocks.login(res.loginSuccessful)
    })
    
    
    cy.fixture("app/authors.json").then((res) => {
      appMocks.fetchAuthors(res.retrieveAuthorsSuccessfully)
      
    })
    
    cy.get("[data-cy='username-input']").type("Oluwadara")
    cy.get("[data-cy='password-input']").type("Oluwadara")
    cy.get("[data-cy='login-btn']").click()

    cy.wait("@login").then((intercept) => {
      expect(intercept.response.statusCode).to.equal(200);
      cy.url().should("include", "/authors");
    });
  })

  it('should log out of the app', () => {
    cy.login()
    cy.get("[data-cy='logout-btn']").click()
    cy.get("[data-cy='username-input']").should('be.visible')
    cy.get("[data-cy='password-input']").should('be.visible')
    cy.get("[data-cy='login-btn']").should('be.visible')
  })
})