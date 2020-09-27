import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import notices from '../store/notices';
import CriticalInfoCard from '../components/index/cards/new_student/critical-info.vue';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();

jest.mock('axios');

describe('Critical Info Card', () => {
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
    const wrapper = mount(CriticalInfoCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.notices).toHaveLength(1);
    expect(wrapper.vm.isResident).toBeTruthy();
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();
  });

  it('Check the filter function - not resident', async () => {
    mockNotices[20].attributes[0].value = 3;
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = mount(CriticalInfoCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.notices).toHaveLength(1);
    expect(wrapper.vm.isResident).toBeFalsy();
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();
  });
});
