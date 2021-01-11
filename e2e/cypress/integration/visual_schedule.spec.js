describe('Visual Schedule - javerage', () => {
  beforeEach(() => {
    cy.intercept('GET', '/api/v1/').as('apiData')
  })

  it('Basic Load - Desktop', () => {
    cy.visit('').then(async () => {
      cy.wait('@apiData').wait(100)
      cy.get('#visual-schedule').scrollIntoView()
    })
  })

  it('Basic Load - Mobile', () => {
    // Pixel 2
    cy.viewport(411, 731);
    cy.visit('').then(async () => {
      cy.wait('@apiData').wait(100)
      cy.get('#visual-schedule').scrollIntoView()
    })
  })
})