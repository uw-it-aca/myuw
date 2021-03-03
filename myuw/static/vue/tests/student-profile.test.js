import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { shallowMount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import profile from '../vuex/store/profile';

import UwCard from '../components/_templates/card.vue';
import StudentProfileCard from '../components/profile/student-profile.vue';
import javg001Profile from './mock_data/profile/javg001.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Student Profile Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        user: {
          affiliations: { 
            employee: true,
            stud_employee: true,
          }
        }
      },
    });
  });

  it('Verify computed properties', async () => {
    axios.get.mockResolvedValue({data: javg001Profile, status: 200});
    const wrapper = shallowMount(StudentProfileCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.profile).toBeTruthy();
  });

  it('addressLocationString()', async () => {
    axios.get.mockResolvedValue({data: javg001Profile, status: 200});
    const wrapper = shallowMount(StudentProfileCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));

    expect(
      wrapper.vm.addressLocationString(wrapper.vm.permanentAddress)
    ).toEqual('Bellevue, WA 98005-1234');

    expect(
      wrapper.vm.addressLocationString({
        city: 'Seattle',
        state: 'WA',
      })
    ).toEqual('Seattle, WA');

    expect(
      wrapper.vm.addressLocationString({
        city: null,
        state: null,
        country: null,
      })
    ).toEqual('');
  });
});
 