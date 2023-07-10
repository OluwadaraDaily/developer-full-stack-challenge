export const fetchAuthors = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "GET", path: "/authors" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("fetchAuthors");
}

export const createAuthor = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "POST", path: "/authors" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("createAuthor");
}

export const getAuthor = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "GET", path: "/authors/*" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("getAuthor");
}

export const updateAuthor = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "PUT", path: "/authors/*" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("updateAuthor");
}

export const getBook = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "GET", path: "/books/*" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("getBook");
}

export const updateBook = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "PUT", path: "/books/*/authors/*" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("updateBook");
}

export const addBook = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "POST", path: "/books/authors/*" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("addBook");
}

export const fetchBooks = (responseBody, statusCode = 200) => {
  cy.intercept(
    { method: "GET", path: "/books" },
    {
      statusCode,
      body: responseBody,
    }
  ).as("fetchBooks");
}