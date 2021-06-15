import axios from 'axios';
import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';

import advisers from '../vuex/store/advisers';
import profile from '../vuex/store/profile';
import javgAdvisers from '../tests/mock_data/advisers/javerage.json';
import javgProfile from '../tests/mock_data/profile/javerage.json';

import AssignedAdviserCard from '../components/academics/adviser.vue';
import UwCard from '../components/_templates/card.vue';

const localVue = createLocalVue(Vuex);
jest.mock('axios');
localVue.component('uw-card', UwCard);

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
          }
        }
      }
    });
  });

  it('Show Assigned Adviser card for undergrad (javerage)', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/advisers/': javgAdvisers,
        '/api/v1/profile/': javgProfile,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.isUndergrad).toBe(true);
    const advisers = wrapper.vm.advisers;
    expect(advisers.length).toBe(5);
    expect(advisers[0].program).toBe("UAA Advising");
    expect(advisers[1].program).toBe("OMAD Advising");
    expect(advisers[2].program).toBe("UW Honors");
    expect(advisers[3].program).toBe("Robinson Center");
    expect(advisers[4].program).toBe("Athletics – SAAS");
  });

  it('Hide Assigned Adviser card if not undergrad', async () => {
    store.state.user.affiliations.undergrad = false;
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('Show error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 543}});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
  });

  it('Hide error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 404}});
    });
    const wrapper = mount(AssignedAdviserCard, {store, localVue,});
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
  });
});