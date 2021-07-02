import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import category_links from '../vuex/store/category_links';
import CalSidebarLinks from '../components/calendar/sidebar-links.vue';
import mockCalLinks from
  './mock_data/category_links/calendar.json';

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
        '/api/v1/categorylinks/pagecalendar': mockCalLinks,
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });

    const wrapper = mount(CalSidebarLinks, { store, localVue });
    await new Promise(setImmediate);

    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.vm.pagecalendarLinks.category_name).toBe("PageCalendar");
    expect(wrapper.vm.pagecalendarLinks.link_data[0].links.length).toBe(4);
  });
});
