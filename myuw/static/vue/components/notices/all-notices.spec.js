import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import notices from '../../vuex/store/notices';
import AllNotices from './all-notices.vue';



import mock_data from './mock.json';

describe('<AllNotices />', () => {
  it('Mount', () => {
    cy.createLocalVue(Vuex).then((localVue) => {
      let store = new Vuex.Store({
        modules: {
          notices,
        }
      });

      cy.intercept(
        {method: 'GET', url: '/api/v1/notices/'},
        mock_data
      )

      mount(AllNotices, {store, localVue});
    });
  })
})