import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import notices from '../../../vuex/store/notices';
import Notices from './notices.vue';

import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/utc'));
dayjs.extend(require('dayjs/plugin/duration'));

// Converts a placeholder data_type `gen_relative_date` into a concrete `date`.
// Can be expanded to generate other placeholder from the mock data.
function generatePlaceHolderInFixture(noticesFixture) {
  noticesFixture.forEach((notice) => {
    notice.attributes.forEach((attr) => {
      switch (attr.data_type) {
        case 'gen_relative_date':
          const offset = parseInt(attr.value);
          let compareTime = dayjs().hour(7).minute(0).second(0).millisecond(0).utc(true);
          compareTime = compareTime.add(dayjs.duration({'days': offset}));
          attr.name = 'Date';
          attr.data_type = 'date';
          attr.value = compareTime.format("YYYY-MM-DD HH:mm:ssZ");
          attr.formatted_date = compareTime.format('ddd, MMM D');
          break;
      }
    });
  });
  return noticesFixture;
}

describe('<Notices />', () => {

  it('Check notices populate and click', () => {
    // Load data from a fixture ('another name for mock data, all fixture are
    // stored inside cypress/fixtures') then use that data
    cy.fixture('notices/javerage.json').then((javerageNotices) => {
      // Sets up the mock response from the notices api
      cy.intercept(
        {method: 'GET', url: '/api/v1/notices/'},
        generatePlaceHolderInFixture(javerageNotices),
      );
    });

    // `createLocalVue` is a custom helper that sets up a local vue instance
    // populated with all the plugins and mixins
    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      // Mount the Notices component with store instance and the localVue
      // instance
      mount(Notices, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here

        // Check the notice groups has the right number of elements
        // `invm` is a custom helper that gets the vm instance of a component
        cy.invm((vm) => vm.isReady).should('be.true');

        // Setup a hook to make sure that notice open puts are being sent
        cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []);
  
        cy.get('button').should('have.length', 8);
        cy.get('.collapse').should('have.length', 8);

        cy.get('.collapse').each(($div, index) => {
            expect($div).to.not.have.class('show');
        });

        cy.get('button').each(($btn, index) => {
            cy.wrap($btn).click();
        });

        cy.get('.collapse').each(($div, index) => {
            expect($div).to.have.class('show');
        });
      });
    });
  });
});