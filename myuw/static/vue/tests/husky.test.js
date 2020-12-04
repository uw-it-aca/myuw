import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import hfs from '../vuex/store/hfs';

import UwCard from '../components/_templates/card.vue';
import HuskyCard from '../components/accounts/husky.vue';
import mockJaverageHfs from './mock_data/hfs.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Husky Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        hfs,
      },
      state: {
        user: {
          affiliations: {
            student: false,
            past_stud: false,
            employee: false,
            past_employee: false,
          }
        }
      }
    });
  });

  it('Display card to student', async () => {
    axios.get.mockResolvedValue({data: mockJaverageHfs, status: 200});
    store.state.user.affiliations.student = true;
    const wrapper = mount(HuskyCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);
    expect(
      wrapper.findAll('h3').at(0).text()
    ).toBe('Husky Card');
    expect(
      wrapper.findAll('h4').at(0).text()
    ).toBe('Student Husky Account');
    expect(
      wrapper.findAll('h4').at(1).text()
    ).toBe('Employee Husky Account');
    expect(wrapper.findAll('span').at(0).text()
    ).toBe('$1.23');
    expect(wrapper.findAll('span').at(2).text()
    ).toBe('$1.00');
    expect(wrapper.findAll('a').length).toBe(1);
  });

  it('Hide card if not the right user type', async () => {
    const wrapper = mount(HuskyCard, { store, localVue });
    expect(wrapper.vm.showCard).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Hide card if api returns 404', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = mount(HuskyCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Show error msg if api returns 543', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = mount(HuskyCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.findAll('a').length).toBe(1);
    expect(wrapper.findAll('a').at(0).attributes().href
    ).toBe('https://hfs.uw.edu/olco/Secure/AccountSummary.aspx');
  });
});
