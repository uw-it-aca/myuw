import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import resources from '../../../vuex/store/resources';
import PinnedResourceCards from './pinned-resource-cards.vue';

describe('<PinnedResourceCards />', () => {

  it('Show Pinned Cards', () => {
    // Load data from a fixture ('another name for mock data, all fixture are
    // stored inside cypress/fixtures') then use that data
    cy.fixture('resources/pinned.json').then((mockPinned) => {
      // Sets up the mock response from the notices api
      cy.intercept(
        {method: 'GET', url: '/api/v1/resources/pinned'},
        mockPinned,
      );

      cy.intercept(
        {method: 'DELETE', url: '/api/v1/resources/academicsadvisingtutoring/pin'},
        mockPinned,
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

      // Mount the AllNotices component with store instance and the localVue
      // instance
      mount(PinnedResourceCards, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here
        
        // Assert that two cards and buttons exist
        cy.get('.card').should('have.length', 2);
        cy.invm((vm) => vm.maybePinnedResources).should('have.length', 1);
        cy.get('button').should('have.length', 2);

        // Click the first 'unpin' button and assert desired effects
        cy.get('button').its(0).click();
        cy.get('.card').should('have.length', 1);
        cy.get('button').should('have.length', 1);
      });
    });
  });
});
