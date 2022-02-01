import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import resources from '../../vuex/store/resources';
import Resources from './resources.vue';

describe('<Resources Page />', () => {

  it('Verify all cards', () => {
    // Load data from a fixture ('another name for mock data, all fixture are
    // stored inside cypress/fixtures') then use that data
    cy.fixture('resources/all.json').then((mockResources) => {
      // Sets up the mock response from the resources api
      cy.intercept(
        {method: 'GET', url: '/api/v1/resources/'},
        mockResources,
      );

      cy.intercept(
        {method: 'DELETE', url: '/api/v1/resources/academicsadvisingtutoring/pin'},
        mockResources,
      );

      cy.intercept(
        {method: 'POST', url: '/api/v1/resources/academicsadvisingtutoring/pin'},
        mockResources,
      );
    });

    // `createLocalVue` is a custom helper that sets up a local vue instance
    // populated with all the plugins and mixins
    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          resources,
        }
      });

      // Mount the Notices component with store instance and the localVue
      // instance
      mount(Resources, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here

        cy.invm((vm) => vm.resources).should('have.length', 9);
        cy.get('.card').should('have.length', 29);
        cy.get('button').should('have.length', 30);

        // Scroll to bottom and click TOP button to take user back
        cy.window().scrollTo('bottom');
        cy.wait(800);
        cy.get('button').last().click();
        cy.window().its('scrollY').should('equal', 0);
        
        // Test pinning and unpinning
        // The 'Advising & Tutoring' card is unpinned by default and is the first card
        cy.get('.card').its(0).find('button').contains('Pin to Home');
        cy.get('.card').its(0).find('button').click();
        cy.get('.card').its(0).find('button').contains('Unpin');
        cy.get('.card').its(0).find('button').click();
        cy.get('.card').its(0).find('button').contains('Pin to Home');

      });
    });
  });
});