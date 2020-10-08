import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import ThankYouCard from '../components/home/cards/new_student/thank-you.vue';

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
    axios.put = jest.fn(() => Promise.resolve());
    const wrapper = mount(ThankYouCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    let htmlDoc = new DOMParser().parseFromString(wrapper.html(), 'text/html');
    expect(htmlDoc.getElementsByClassName('myuw-thank-you-notices')[0]
           .getElementsByTagName('div').length).toBe(2);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.notices).toHaveLength(0);
    expect(wrapper.vm.showThankYou(mockNotices)).toBeTruthy();
  });

  it('Check the filter function - after notices read', async () => {
    mockNotices[5].is_read = true;
    mockNotices[22].is_read = true;
    axios.get.mockResolvedValue({data: mockNotices});
    axios.put = jest.fn(() => Promise.resolve());
    const wrapper = mount(ThankYouCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.notices).toHaveLength(0);
    expect(wrapper.vm.showThankYou(mockNotices)).toBeFalsy();
  });

  // it('Check the filter function - default', async () => {
  //   axios.get.mockResolvedValue({data: mockNotices});
  //   const wrapper = mount(ThankYouCard, {store, localVue});
  //   // It takes like 10 ms to process the mock data through fetch postProcess
  //   await new Promise((r) => setTimeout(r, 10));
  //   expect(wrapper.vm.isReady).toBeTruthy();
  //   expect(wrapper.vm.notices).toHaveLength(2);
  // });
});
