import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import directory from '../vuex/store/directory';

import UwCard from '../components/_templates/card.vue';
import EmployeeProfileCard from '../components/profile/employee-profile.vue';
import javerageDirectory from './mock_data/directory/javerage.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Employee Profile Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        directory,
      },
      state: {
        user: {
          affiliations: { 
            employee: true,
            stud_employee: true,
            tacoma: false,
          }
        }
      },
    });
  });

  it('Verify computed properties', async () => {
    axios.get.mockResolvedValue({data: javerageDirectory, status: 200});
    const wrapper = mount(EmployeeProfileCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.noFormsOfContact).toBe(false);
  });
});
 