// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('overrideUserAndDate', (username, datetime) => {
  cy.log('overrideUserAndDate')
  return cy.url({log: false}).then(async (currentUrl) => {
    if (username) {
      await cy.visit('http://localhost:8000/support').then(() => {
        cy.get('input[name=override_as]')
          .type(username)
        cy.get('button.btn.btn-block.btn-primary[type=submit]')
          .click()
      })
    }
    if (datetime) {
      await cy.visit('http://localhost:8000/admin/dates').then(() => {
        cy.get('input[name=date]')
          .clear()
          .type(datetime.format('YYYY-MM-DD HH:mm:ss'))
        cy.get('button.btn.btn-primary[type=submit]')
          .click()
      })
    }
    return cy.visit(currentUrl)
  })
})

Cypress.Commands.add('clearOverride', () => {
  cy.log('clearOverride')
  return cy.url({log: false}).then(async (currentUrl) => {
    await cy.visit('http://localhost:8000/support').then(() => {
      cy.get('button.btn.btn-block.btn-danger[type=submit]')
        .click()
    })
    await cy.visit('http://localhost:8000/admin/dates').then(() => {
      cy.get('input[name=date]')
        .clear()
      cy.get('button.btn.btn-primary[type=submit]')
        .click()
    })
    return cy.visit(currentUrl)
  })
})

Cypress.Commands.add('waitn', (interceptName, n) => {
  cy.log(`waiting for ${interceptName} ${n} times`)
  let wait = cy.wait(interceptName, {log: false});
  for (let i = 0; i < n - 1; i++) {
    wait = wait.then(() => cy.wait(interceptName, {log: false}))
  }
  return wait
})