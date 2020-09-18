import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import notices from '../store/notices';
import ThankYouCard from '../components/index/cards/new_student/thank-you.vue';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

jest.mock('axios');

describe('Thank You Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        }
      }
    });
  });

  it('Check the filter function - default', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = mount(ThankYouCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.unreadNotices()).toHaveLength(2);
  });

  it('Check the filter function - after notices read', async () => {
    mockNotices[5].is_read = true;
    mockNotices[22].is_read = true;
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = mount(ThankYouCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.unreadNotices()).toHaveLength(0);
  });
});
