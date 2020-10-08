import axios from 'axios';
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import profile from '../vuex/store/profile';
import UWNetidCard from '../components/pages/index/cards/accounts/uwnetid.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

import mockProfileData from './mock_data/profile/jinter.json';

const localVue = createLocalVue();

library.add(faExclamationTriangle);

localVue.component('font-awesome-icon', FontAwesomeIcon);

jest.mock('axios');

describe('UWNetID Card', () => {
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
            applicant: false,
            employee: false,
            '2fa_permitted': true,
          }
        }
      }
    });
  });

  it('Check status changes on fetch', async () => {
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = shallowMount(UWNetidCard, {store, localVue});
    expect(
        profile.getters.isFetching(wrapper.vm.$store.state.profile),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        profile.getters.isReady(wrapper.vm.$store.state.profile),
    ).toBeTruthy();
    expect(
        profile.getters.isErrored(wrapper.vm.$store.state.profile),
    ).toBeFalsy();
  });

  it('Check status when fetch fails', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = shallowMount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        profile.getters.isErrored(wrapper.vm.$store.state.profile),
    ).toBeTruthy();
    expect(
        profile.getters.isReady(wrapper.vm.$store.state.profile),
    ).toBeFalsy();
  });

  it('Check showCard method', async () => {
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.showCard).toBeFalsy();
  });

  it('Display card with 2-factor-auth', async () => {
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.showCard).toBeTruthy();
    expect(wrapper.vm.two_factor).toBeTruthy();
    expect(wrapper.findAll('li')).toHaveLength(3);
    expect(wrapper.vm.data).toBeDefined();
  });

  it('Show custom error msg for 543', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = shallowMount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.showError).toBeTruthy();
  });
});
