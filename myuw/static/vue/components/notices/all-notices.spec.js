import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import notices from '../../vuex/store/notices';
import AllNotices from './all-notices.vue';

describe('<AllNotices />', () => {
  it('Mount', () => {
    // Can also use 
    // cy.fixture('notices/javerage.json').then((javerageNotices) => {
    //   cy.intercept({method: 'GET', url: '/api/v1/notices/'}, javerageNotices);
    // });
    cy.intercept('GET', '/api/v1/notices/', { fixture: 'notices/javerage.json' });
    

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      mount(AllNotices, {store, localVue});

      cy.intercept('PUT', '/api/v1/notices/', {times: 8}).as('openAllNotices');
      cy.get('a').first().click();
      cy.wait('@openAllNotices');
    });
  })
})