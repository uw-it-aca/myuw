import axios from 'axios';

import { createLocalVue } from './helper';
import { mount } from '@vue/test-utils';
import hxt from '../vuex/store/hx_toolkit';
import Vuex from 'vuex';

import UwCard from '../components/_templates/card.vue';
import HxtCard from '../components/_common/husky-experience.vue';
import mockHxt from './mock_data/husky-exp/husky-experience.html';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Hxt Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'hx_toolkit': hxt,
      },
      state: {
        user: {
          affiliations: {
            hxt_viewer: false,
          }
        }
      }
    });
  });

  it('Display card if user is hxt_viewer', async () => {
    store.state.user.affiliations.hxt_viewer = true;
    axios.get.mockResolvedValue({data: mockHxt, status: 200});
    const wrapper = mount(HxtCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.statusCode).toBe(200);
    expect(wrapper.vm.hxtViewer).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });

  it('Hide card if not hxt_viewer', async () => {
    axios.get.mockResolvedValue({data: mockHxt, status: 200});
    const wrapper = mount(HxtCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.vm.hxtViewer).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Hide card if api returns 404', async () => {
    store.state.user.affiliations.hxt_viewer = true;
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = mount(HxtCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.hxtViewer).toBe(true);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.statusCode).toBe(404);
    expect(wrapper.vm.showError).toBe(false);
  });

  it('Show error msg if api returns 543', async () => {
    store.state.user.affiliations.hxt_viewer = true;
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = mount(HxtCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.hxtViewer).toBe(true);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.statusCode).toBe(543);
    expect(wrapper.vm.showError).toBe(true);
  });
});
