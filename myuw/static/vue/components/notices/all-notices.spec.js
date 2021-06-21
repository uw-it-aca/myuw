import { mount } from '@cypress/vue';
import { createLocalVue } from '@vue/test-utils';


import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';

import notices from '../../vuex/store/notices';
import AllNotices from './all-notices.vue';

import '../../../css/myuw/custom.scss';
import '../../../css/myuw/global.scss';
import mock_data from './mock.json';

describe('<AllNotices />', () => {
  it('Mount', () => {
    let localVue = createLocalVue();
    localVue.component('font-awesome-icon', FontAwesomeIcon);
    localVue.use(BootstrapVue);
    localVue.use(Vuex);
    let store = new Vuex.Store({
      modules: {
        notices,
      }
    });

    cy.intercept(
      {method: 'GET', url: '/api/v1/notices/'},
      // mock_data
      []
    )

    mount(AllNotices, {store, localVue});

    cy.wait(3000);
  })
})