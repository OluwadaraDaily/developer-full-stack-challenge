import * as authMocks from "./mocks/auth";
import * as appMocks from "./mocks/app";

Cypress.Commands.add('login', () => {
  cy.visit('/')
  
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