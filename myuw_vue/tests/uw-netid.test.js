import axios from 'axios';
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import profile from '../vuex/store/profile';
import UWNetidCard from '../components/_common/uw-netid.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

import mockProfileData from './mock_data/profile/jinter.json';

const localVue = createLocalVue(Vuex);

library.add(faExclamationTriangle);

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
            instructor: false,
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
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
    expect(
        profile.getters.isErrored(wrapper.vm.$store.state.profile),
    ).toBeTruthy();
    expect(
        profile.getters.isReady(wrapper.vm.$store.state.profile),
    ).toBeFalsy();
  });

  it('Check showCard on Accounts page for applicant', async () => {
    store.state.user.affiliations.applicant = true;
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
  });

  it('Check showCard on Accounts page for instructor', async () => {
    store.state.user.affiliations.instructor = true;
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
  });

  it('Check showCard on Accounts page for student', async () => {
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
  });

  it('Check showCard on Home page', async () => {
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {
      store, localVue, propsData: {
        isHomePage: true,
      }});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
  });

  it('Display card with 2-factor-auth', async () => {
    axios.get.mockResolvedValue({data: mockProfileData, status: 200});
    const wrapper = mount(UWNetidCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
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
    await new Promise(setImmediate);
    expect(wrapper.vm.showError).toBeTruthy();
  });
});
