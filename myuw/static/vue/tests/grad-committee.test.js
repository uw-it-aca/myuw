import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import grad from '../vuex/store/grad';

import GradCommittee from '../components/academics/grad-committee.vue';

import sea_grad from './mock_data/sea_grad.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Grad-Committee Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        grad,
      },
      state: {
        user: {
          affiliations: {
            grad: true,
          }
        }
      }
    });
  });

  it('Computed Properties for grad (seagrad)', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/grad/': sea_grad,
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });

    const wrapper = mount(GradCommittee, { store, localVue });
    await new Promise(setImmediate);

    expect(wrapper.vm.committees).toBeTruthy();
    expect(wrapper.vm.committees.length).toBe(3);
    expect(wrapper.vm.showCard).toBe(true);
  });

  it('Hide if not grad', async () => {
    store.state.user.affiliations.grad = false;
    const wrapper = mount(GradCommittee, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('Show error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 543}});
    });
    const wrapper = mount(GradCommittee, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
  });

  it('Hide card no committee data', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/grad/': { committees: null },
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });
    const wrapper = mount(GradCommittee, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(false);
  });

  it('formatMemberString()', async () => {
    const wrapper = mount(GradCommittee, {store, localVue});
    await new Promise(setImmediate);

    let exampleMember = {
			first_name: 'Bet',
			last_name: 'Duncan',
			member_type: 'Chair',
			reading_type: 'Reading Committee Chair',
			dept: 'Anthropology',
			email: 'bbb@u.washington.edu',
			status: 'active'
		}

    expect(
      wrapper.vm.formatMemberString(exampleMember)
    ).toEqual('Bet Duncan, Chair, Reading Committee Chair');

    exampleMember.reading_type = null;
    expect(
      wrapper.vm.formatMemberString(exampleMember)
    ).toEqual('Bet Duncan, Chair');

    exampleMember.member_type = null;
    expect(
      wrapper.vm.formatMemberString(exampleMember)
    ).toEqual('Bet Duncan');

    exampleMember.reading_type = 'Reading Committee Chair';
    expect(
      wrapper.vm.formatMemberString(exampleMember)
    ).toEqual('Bet Duncan, Reading Committee Chair');
  });
});
