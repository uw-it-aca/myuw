import axios from 'axios';
import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';

import advisers from '../vuex/store/advisers';
import profile from '../vuex/store/profile';
import javgAdvisers from './mock_data/advisers/javerage.json';
import inactiveAdvisers from './mock_data/advisers/jbot.json';
import javgProfile from './mock_data/profile/javerage.json';
import jintProfile from './mock_data/profile/jinter.json';

import AssignedAdviserCard from '../components/academics/adviser.vue';
import UwCard from '../components/_templates/card.vue';
import UwCardProperty from '../components/_templates/card-property.vue';

const localVue = createLocalVue(Vuex);
jest.mock('axios');

describe('Assigned Adviser Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        advisers,
        profile,
      },
      state: {
        user: {
          affiliations: {
            undergrad: true,
            stud_employee: false,
            grad: false,
          }
        }
      }
    });
  });

  it('Show Adviser card for undergrad (javerage)', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/advisers/': javgAdvisers,
        '/api/v1/profile/': javgProfile,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.hasAdviser).toBe(true);
    expect(wrapper.vm.hasProfile).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCardProperty)).toHaveLength(2);
    expect(wrapper.vm.hasMajors).toBe(true);
    expect(wrapper.vm.hasMinors).toBe(true);
  });

  it('Show card has profile but no Assigned Adviser (jbot)', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/advisers/': inactiveAdvisers,
        '/api/v1/profile/': javgProfile,
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(AssignedAdviserCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.hasAdviser).toBe(false);
    expect(wrapper.vm.hasProfile).toBe(true);
    expect(wrapper.vm.hasMajors).toBe(true);
    expect(wrapper.vm.hasMinors).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCardProperty)).toHaveLength(2);
  });

  it('Hide Adviser card if not undergrad', async () => {
    store.state.user.affiliations.undergrad = false;
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('Hide Adviser card if is a student employee and grad', async () => {
    store.state.user.affiliations.stud_employee = true;
    store.state.user.affiliations.grad = true;
    store.state.user.affiliations.undergrad = false;
    const wrapper = mount(AssignedAdviserCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.shouldLoad).toBe(false);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('Hide Adviser card if class level is not desired', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/advisers/': inactiveAdvisers,
        '/api/v1/profile/': jintProfile,
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(AssignedAdviserCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.hasProfile).toBe(false);
    expect(wrapper.vm.showContent).toBe(false);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('Show card if no adviser record', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/v1/advisers/') {
        return Promise.reject({response: {status: 404}});
      }
      const urlData = {
        '/api/v1/profile/': javgProfile,
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.hasAdviser).toBe(false);
    expect(wrapper.vm.hasProfile).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
  });

  it('Show error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 543}});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });

  it('Hide error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 404}});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue,});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false);
    expect(wrapper.vm.showError).toBe(false);
    expect(wrapper.vm.hasAdviser).toBe(false);
    expect(wrapper.vm.hasProfile).toBe(false);
  });
});
