import axios from 'axios';

import { createLocalVue } from './helper';
import { mount } from '@vue/test-utils';

import Vuex from 'vuex';
import hfs from '../vuex/store/hfs';

import UwCard from '../components/_templates/card.vue';
import HfsSeaCard from '../components/accounts/hfs-sea.vue';
import mockJaverageHfs from './mock_data/hfs.json';

const localVue = createLocalVue(Vuex);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('HFS Sea Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        hfs,
      },
      state: {
        user: {
          affiliations: {
            grad: false,
            seattle: false,
            undergrad: false,
          }
        }
      }
    });
  });

  it('Display card if user is seattle student', async () => {
    store.state.user.affiliations.undergrad = true;
    store.state.user.affiliations.seattle = true;
    axios.get.mockResolvedValue({data: mockJaverageHfs, status: 200});
    const wrapper = mount(HfsSeaCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);
    expect(
      wrapper.findAll('h2').at(0).text()
    ).toBe('Housing & Food Services');
    expect(
      wrapper.findAll('h3').at(0).text()
    ).toBe('Dining Balance');
    expect(
      wrapper.findAll('h3').at(1).text()
    ).toBe('Explore Campus Housing');
    expect(
      wrapper.findAll('h3').at(2).text()
    ).toBe('Manage Account');
    expect(
      wrapper.findAll('h3').at(3).text()
    ).toBe('Resident Resources');
    expect(wrapper.findAll('span').at(0).text()
    ).toBe('$5.10');
    expect(wrapper.findAll('a').length).toBe(10);
  });

  it('Hide card if not a seattle student', async () => {
    axios.get.mockResolvedValue({data: mockJaverageHfs, status: 200});
    const wrapper = mount(HfsSeaCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false)
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Hide card if api returns 404', async () => {
    store.state.user.affiliations.grad = true;
    store.state.user.affiliations.seattle = true;
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = mount(HfsSeaCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
  });

  it('Show error msg if api returns 543', async () => {
    store.state.user.affiliations.undergrad = true;
    store.state.user.affiliations.seattle = true;
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = mount(HfsSeaCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.findAll('a').length).toBe(1);
    expect(wrapper.findAll('a').at(0).attributes().href
    ).toBe('https://hfs.uw.edu/myhfs/account.aspx');
  });
});
