const dayjs = require('dayjs');

describe('My First Test', () => {
  it('Load Page!', () => {
    cy.intercept('GET', '/api/v1').as('apiData');
    cy.visit('').then(async () => {
      await cy.waitn('@apiData', 12)
      cy.wait(1000)
      cy.get('#visual-schedule').scrollIntoView()
    })
  })
  // it('Load Page! - 2', () => {
  //   cy.visit('').then(async () => {
  //     await cy.overrideUserAndDate('bill', dayjs('2020-02-11 10:20'))
  //   })
  // })
})