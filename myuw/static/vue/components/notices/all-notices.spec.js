import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import notices from '../../vuex/store/notices';
import AllNotices from './all-notices.vue';

import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/utc'));
dayjs.extend(require('dayjs/plugin/duration'));

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
  it('No notices', () => {
    cy.intercept('GET', '/api/v1/notices/', []);

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      mount(AllNotices, {store, localVue}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);
        // TODO: take image snapshot here
      });
    });
  });

  it('javerage', () => {
    cy.fixture('notices/javerage.json').then((javerageNotices) => {
      cy.intercept(
        {method: 'GET', url: '/api/v1/notices/'},
        generatePlaceHolderInFixture(javerageNotices),
      );
    });

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      mount(AllNotices, {store, localVue}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here
        // Check the notice groups has the right elements
        cy.invm((vm) => vm.noticeGroups).its(0).its(1).should('have.length', 7);
        cy.invm((vm) => vm.noticeGroups).its(3).its(1).should('have.length', 1);

        // Intercept the notice open messages
        cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []);
  
        // Both groups are collapsed
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "false");

        // Expand frist group
        cy.get('div[role="button"]').its(0).click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "true");

        // Collapse frist group
        cy.get('div[role="button"]').its(0).click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");

        // Expand both groups
        cy.get('a').first().click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "true");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "true");

        // Collapse both groups
        cy.get('a').first().click();
        cy.get('div[role="button"]').its(0).should('have.attr', "aria-expanded", "false");
        cy.get('div[role="button"]').its(1).should('have.attr', "aria-expanded", "false");
      });
    });
  });

  it('notice open observer', () => {
    cy.fixture('notices/javerage.json').then((javerageNotices) => {
      cy.intercept(
        {method: 'GET', url: '/api/v1/notices/'},
        generatePlaceHolderInFixture(javerageNotices),
      );
    });

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      mount(AllNotices, {store, localVue}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // Intercept the notice open messages
        cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []).as('openNotice');
  
        // Expand everthing
        cy.get('a').first().click();

        cy.invm((vm) => vm.noticeGroups).then((groups) => {
          let shouldShowNoticeHashes = groups
            .flatMap((group) => group[1])
            .map((notice) => notice.id_hash);

          let shownNoticeHashes = [];
          cy.get('div.bg-white.mb-2.p-3').each(($el) => {
            cy.wrap($el).scrollIntoView();
            cy.wait('@openNotice')
              .then((req) => shownNoticeHashes.push(req.request.body.notice_hashes[0]));
          });

          cy.wrap(shownNoticeHashes).should('have.members', shouldShowNoticeHashes);
        });
      });
    });
  });
});