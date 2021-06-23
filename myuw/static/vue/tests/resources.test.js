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

  it('Verify all cards', async () => {
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
    axios.post.mockImplementation((url) => {
      const urlData = {
        '/api/v1/resources/academicsadvisingtutoring/pin': mockRes,
      };
      return Promise.resolve({data: urlData[url]});
    });
    let wrapper = mount(Resources, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.findComponent(Resources).exists()).toBe(true);
    expect(wrapper.vm.resources.length).toBe(9);
    expect(wrapper.findAllComponents(ResourceCard).length).toBe(9);
    expect(wrapper.findAllComponents(UwCard).length).toBe(29);
    expect(wrapper.findAll('button').length).toBe(30);
    await wrapper.findAll('button').at(29).trigger('click');
    expect(spyScrollTo).toHaveBeenCalledWith({
      top: 0,
      behavior: 'smooth',
    });

    // Test Pin
    const resUnpinned = wrapper.vm.resources[0];
    const resPinned = wrapper.vm.resources[0];
    wrapper = mount(ResourceCard,
      {store, localVue, propsData: {'resource': resUnpinned}});
    await new Promise(setImmediate);
    expect(wrapper.findAllComponents(UwCard).length).toBe(5);
    expect(wrapper.findAll('button').length).toBe(5);
    expect(wrapper.findAll('button').at(0).text()).toBe("Pin to Home");
    await wrapper.findAll('button').at(0).trigger('click');
    expect(wrapper.findAll('button').at(0).text()).toBe("Unpin");

    wrapper = mount(ResourceCard,
      {store, localVue, propsData: {'resource': resPinned}});
    await new Promise(setImmediate);
    expect(wrapper.findAll('button').at(0).text()).toBe("Unpin");
    await wrapper.findAll('button').at(0).trigger('click');
    expect(wrapper.findAll('button').at(0).text()).toBe("Pin to Home");
  });
});
