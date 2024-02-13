import axios from 'axios';
import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import resources from '../vuex/store/resources';
import mockRes from './mock_data/resources/pinned.json';

import UwCard from '../components/_templates/card.vue';
import PinnedResources from '../components/home/resources/pinned-resource-cards.vue';

const localVue = createLocalVue(Vuex);
jest.mock('axios');

describe('Pinned Resources Card', () => {
  let store;
  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        resources,
      },
    });
  });

  it('Show Pinned cards', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/resources/pinned/': mockRes,
      };
      return Promise.resolve({data: urlData[url]});
    });
    axios.delete.mockImplementation((url) => {
      const urlData = {
        '/api/v1/resources/academicsadvisingtutoring/pin': mockRes,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(PinnedResources, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.findComponent(PinnedResources).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCard).length).toBe(2);
    expect(wrapper.vm.maybePinnedResources.length).toBe(1);
    expect(wrapper.findAll('button')).toHaveLength(2);
    await wrapper.findAll('button').at(0).trigger('click');
    expect(wrapper.findAllComponents(UwCard).length).toBe(1);
    expect(wrapper.findAll('button')).toHaveLength(1);
  });
});
