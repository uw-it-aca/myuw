import axios from 'axios';
import {mount} from '@vue/test-utils';
import {createLocalVue} from './helper';
import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import SummerEFSCard from '../components/home/new_student/summer-efs.vue';
import mockNotices from './mock_data/notice/javg004.json';

const localVue = createLocalVue(Vuex);

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
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.notices).toHaveLength(1);
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();
  });
});
