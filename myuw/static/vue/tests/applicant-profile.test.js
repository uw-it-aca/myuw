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
import ApplicantProfileCard from '../components/profile/applicant-profile.vue';
import japplicantProfile from './mock_data/profile/japplicant.json';

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
        user: {
          affiliations: {
            student: false,
            applicant: true,
          }
        }
      },
    });
  });

  it('Verify computed properties for japplicant', async () => {
    axios.get.mockResolvedValue({data: japplicantProfile, status: 200});
    const wrapper = shallowMount(ApplicantProfileCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.profile).not.toBe(null);
    expect(wrapper.vm.email).toBe('japplicant@u.washington.edu');
    expect(wrapper.vm.showCard).toBeTruthy();
  });

  it('addressLocationString()', async () => {
    axios.get.mockResolvedValue({data: japplicantProfile, status: 200});
    const wrapper = shallowMount(ApplicantProfileCard, {store, localVue});
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
