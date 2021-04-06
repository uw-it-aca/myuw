import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import directory from '../vuex/store/directory';

import UwCard from '../components/_templates/card.vue';
import EmployeeProfileCard from '../components/profile/employee-profile.vue';
import javerageDirectory from './mock_data/directory/javerage.json';

const localVue = createLocalVue(Vuex);
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
    await new Promise(setImmediate);

    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.noFormsOfContact).toBe(false);
  });
});
 