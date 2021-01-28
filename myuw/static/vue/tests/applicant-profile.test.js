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
import ApplicantProfileCard from '../components/accounts/applicant-profile.vue';
import mockJinterProfile from './mock_data/profile/jinter.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Applicant Profile Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        
      }
    });
  });

  it('Verify computed properties for japplicant', async () => {
    // axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    // const wrapper = shallowMount(MedicineAccountCard, {store, localVue});
    // await new Promise((r) => setTimeout(r, 10));
    // expect(wrapper.vm.showCard).toBe(false);
    // expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('addressLocationString()', () => {
    // axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    // const wrapper = mount(MedicineAccountCard, {store, localVue});

    // expect(
    //   wrapper.vm.toFriendlyDate('2020-08-24')
    // ).toEqual('Mon, Aug 24');

    // expect(
    //   wrapper.vm.toFriendlyDate(undefined)
    // ).toEqual('');
    // expect(
    //   wrapper.vm.toFriendlyDate('')
    // ).toEqual('');
  });
});
