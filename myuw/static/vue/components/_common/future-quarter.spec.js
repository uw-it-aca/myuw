import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import oquarter from '../../vuex/store/oquarter';
import FutureQuarter from './future-quarter.vue';

import dayjs from 'dayjs';

// function generatePlaceHolderInFixture(noticesFixture) {
//   noticesFixture.forEach((notice) => {
//     notice.attributes.forEach((attr) => {
//       switch (attr.data_type) {
//         case 'gen_relative_date':
//           const offset = parseInt(attr.value);
//           let compareTime = dayjs().hour(7).minute(0).second(0).millisecond(0).utc(true);
//           compareTime = compareTime.add(dayjs.duration({'days': offset}));
//           attr.name = 'Date';
//           attr.data_type = 'date';
//           attr.value = compareTime.format("YYYY-MM-DD HH:mm:ssZ");
//           attr.formatted_date = compareTime.format('ddd, MMM D');
//           break;
//       }
//     });
//   });
//   return noticesFixture;
// }

describe('<FutureQuarter />', () => {
  it('No oquarter', () => {
    cy.intercept('GET', '/api/v1/oquarters/', { statusCode: 543 });

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          oquarter,
        },
        state: {
          user: {
            affiliations: {
              student: true,
            }
          }
        }
      });

      mount(FutureQuarter, {store, localVue, propsData: { highlighted: true }}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);
        // TODO: take image snapshot here
      });
    });
  });

  it('javerage', () => {
    cy.fixture('oquarter/javerage.json').then((javerageOquarter) => {
      cy.intercept(
        {method: 'GET', url: '/api/v1/oquarters/'},
        javerageOquarter
      );
    });

    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          oquarter,
        },
        state: {
          user: {
            affiliations: {
              student: true,
            }
          }
        }
      });

      mount(FutureQuarter, {store, localVue, propsData: { highlighted: true }}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

        // TODO: take image snapshot here
        // Check the notice groups has the right elements
        
      });
    });
  });

  // it('notice open observer', () => {
  //   cy.fixture('notices/javerage.json').then((javerageNotices) => {
  //     cy.intercept(
  //       {method: 'GET', url: '/api/v1/notices/'},
  //       generatePlaceHolderInFixture(javerageNotices),
  //     );
  //   });

  //   cy.createLocalVue(Vuex).then((localVue) => {
  //     let store = new Vuex.Store({
  //       modules: {
  //         notices,
  //       }
  //     });

  //     mount(AllNotices, {store, localVue}).then(() => {
  //       cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);

  //       // Intercept the notice open messages
  //       cy.intercept({method: 'PUT', url: '/api/v1/notices/', times: 8}, []).as('openNotice');
  
  //       // Expand everthing
  //       cy.get('a').first().click();

  //       cy.invm((vm) => vm.noticeGroups).then((groups) => {
  //         let shouldShowNoticeHashes = groups
  //           .flatMap((group) => group[1])
  //           .map((notice) => notice.id_hash);

  //         let shownNoticeHashes = [];
  //         cy.get('div.bg-white.mb-2.p-3').each(($el) => {
  //           cy.wrap($el).scrollIntoView();
  //           cy.wait('@openNotice')
  //             .then((req) => shownNoticeHashes.push(req.request.body.notice_hashes[0]));
  //         });

  //         cy.wrap(shownNoticeHashes).should('have.members', shouldShowNoticeHashes);
  //       });
  //     });
  //   });
  // });
});