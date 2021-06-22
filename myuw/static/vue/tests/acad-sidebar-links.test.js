import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import category_links from '../vuex/store/category_links';

import AcadSidebarLinks from '../components/academics/sidebar-links.vue';

import academicLinks from './mock_data/category_links/academics/javerage.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Academic Sidebar Links', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        category_links,
      },
    });
  });

  it('Computed Properties', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/categorylinks/pageacademics': academicLinks,
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });

    const wrapper = mount(AcadSidebarLinks, { store, localVue });
    await new Promise(setImmediate);

    expect(wrapper.vm.linkData).toBeTruthy();
    expect(wrapper.vm.linkData.length).toBe(6);
  });
});
