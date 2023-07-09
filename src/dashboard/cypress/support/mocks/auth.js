export const login = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "POST", path: "/token" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("login");
};