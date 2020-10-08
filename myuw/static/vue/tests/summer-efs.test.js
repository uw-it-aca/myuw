import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import SummerEFSCard from
  '../components/index/cards/new_student/summer-efs.vue';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

jest.mock('axios');

describe('Summer EFS Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
      },
      state: {},
    });
  });

  it('Summer EFS - default', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = mount(SummerEFSCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.notices).toHaveLength(1);
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();
  });
});
