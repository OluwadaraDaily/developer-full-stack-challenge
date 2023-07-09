import * as authMocks from "../support/mocks/auth";

describe('My First Test', () => {
  beforeEach(() => {
    console.log('CY ->', cy)
    cy.visit("/");
  })
  it('Does not do much!', () => {
    cy.get("[data-cy='username-input']").type("Oluwadara")
    cy.get("[data-cy='password-input']").type("Oluwadara")

    cy.fixture("auth/login.json").then((res) => {
      
    })
  })
})