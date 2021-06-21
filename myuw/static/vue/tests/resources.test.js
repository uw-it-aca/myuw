import axios from 'axios';
import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import resources from '../vuex/store/resources';
import mockRes from './mock_data/resources/all.json';

import UwCard from '../components/_templates/card.vue';
import Resources from '../components/resources/resources.vue';
import ResourceCard from '../components/resources/resource-card.vue';

const localVue = createLocalVue(Vuex);
localVue.component('uw-card', UwCard);
jest.mock('axios');
const spyScrollTo = jest.fn();
Object.defineProperty(global.window, 'scrollTo', { value: spyScrollTo });

describe('Resources Page Content', () => {
  let store;
  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        resources,
      },
    });
    Object.defineProperty(global.window, 'scrollTo', { value: spyScrollTo });
    spyScrollTo.mockClear();
  });

  it('Show cards', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/resources/': mockRes,
      };
      return Promise.resolve({data: urlData[url]});
    });
    axios.delete.mockImplementation((url) => {
      const urlData = {
        '/api/v1/resources/academicsadvisingtutoring/pin': mockRes,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(Resources, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.findComponent(Resources).exists()).toBe(true);
    expect(wrapper.vm.resources.length).toBe(9);
    expect(wrapper.findAllComponents(ResourceCard).length).toBe(9);
    expect(wrapper.findAllComponents(UwCard).length).toBe(29);
    expect(wrapper.findAll('button').length).toBe(30);
    console.log(wrapper.findAll('button').at(29));
    await wrapper.findAll('button').at(29).trigger('click');
    expect(spyScrollTo).toHaveBeenCalledWith({
      top: 0,
      behavior: 'smooth',
    });
  });
});
