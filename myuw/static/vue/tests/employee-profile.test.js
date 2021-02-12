import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { shallowMount } from '@vue/test-utils';
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
            staticUrl: './',
          }
        }
      },
    });
  });

  it('Verify computed properties', async () => {
    debugger;
    axios.get.mockResolvedValue({data: javerageDirectory, status: 200});
    debugger;
    const wrapper = shallowMount(EmployeeProfileCard, {store, localVue});
    debugger;
    await new Promise((r) => setTimeout(r, 10));

    //expect(wrapper.vm.showCard).toBeFalsy();
    expect(wrapper.vm.position).toBeFalsy();
    
  });
});
 