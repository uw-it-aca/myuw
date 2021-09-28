import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import notices from '../../vuex/store/notices';
import AllNotices from './all-notices.vue';

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

describe('<AllNotices />', () => {
  // Testing the condition where there are no notices.
  it('No notices', () => {
    // Sets up the mock response from the notices api to be `[]`
    cy.intercept('GET', '/api/v1/notices/', []);

    // `createLocalVue` is a custom helper that sets up a local vue instance
    // populated with all the plugins and mixins
    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      // Mount the AllNotices component with store instance and the localVue
      // instance
      mount(AllNotices, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true 
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);
        // TODO: take image snapshot here
      });
    });
  });

  it('javerage', () => {
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

      // Mount the AllNotices component with store instance and the localVue
      // instance
      mount(AllNotices, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here

        // Check the notice groups has the right number of elements
        // `invm` is a custom helper that gets the vm instance of a component
        cy.invm((vm) => vm.noticeGroups).its(0).its(1).should('have.length', 7);
        cy.invm((vm) => vm.noticeGroups).its(3).its(1).should('have.length', 1);

        // Setup a hook to make sure that notice open puts are being sent
        cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []);
  
        // Both groups are collapsed
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "false");

        // Expand frist group
        cy.get('div[role="button"]').its(0).click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "true");
        cy.get('div[role="button"]').its(0).siblings().its(0).should('have.class', 'show');

        // Collapse frist group
        cy.get('div[role="button"]').its(0).click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(0).siblings().its(0).should('not.have.class', 'show');
        cy.get('div[role="button"]').its(0).siblings().its(0).should('not.have.class', 'collapsing');
        cy.get('div[role="button"]').its(0).siblings().its(0).should('have.class', 'collapse');

        // Expand both groups
        cy.get('a').first().click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "true");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "true");
        cy.get('div[role="button"]').its(0).siblings().its(0).should('have.class', 'show');
        cy.get('div[role="button"]').its(1).siblings().its(0).should('have.class', 'show');

        // Collapse both groups
        cy.get('a').first().click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(0).siblings().its(0).should('not.have.class', 'show');
        cy.get('div[role="button"]').its(0).siblings().its(0).should('not.have.class', 'collapsing');
        cy.get('div[role="button"]').its(0).siblings().its(0).should('have.class', 'collapse');
        cy.get('div[role="button"]').its(1).siblings().its(0).should('not.have.class', 'show');
        cy.get('div[role="button"]').its(1).siblings().its(0).should('not.have.class', 'collapsing');
        cy.get('div[role="button"]').its(1).siblings().its(0).should('have.class', 'collapse');
      });
    });
  });

  it('notice open observer', () => {
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

      // Mount the AllNotices component with store instance and the localVue
      // instance
      mount(AllNotices, {store, localVue}).then(() => {
        // A custom helper that will wait for a components card to have some condition
        // in this case the card's isReady or isErrored needs to be true
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // Intercept the notice open messages and name that intercept `openNotice`
        cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []).as('openNotice');
  
        // Expand everthing
        cy.get('a').first().click();

        // This goes though each notice and waits for the notice open put to be sent.
        cy.invm((vm) => vm.noticeGroups).then((groups) => {
          let shouldShowNoticeHashes = groups
            .flatMap((group) => group[1])
            .map((notice) => notice.id_hash);

          let shownNoticeHashes = [];
          cy.get('div.bg-white.mb-2.p-3').each(($el) => {
            cy.wrap($el).scrollIntoView();
            // Waits for the notice open here
            cy.wait('@openNotice')
              .then((req) => shownNoticeHashes.push(req.request.body.notice_hashes[0]));
          });

          cy.wrap(shownNoticeHashes).should('have.members', shouldShowNoticeHashes);
        });
      });
    });
  });
});