import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import notices from '../vuex/store/notices';
import ToRegisterCard from '../components/home/new_student/to-register.vue';

import mockNotices from './mock_data/notice/javg004.json';
import interNotices from './mock_data/notice/jinter.json';
import bothellNotices from './mock_data/notice/jbothell.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('To Register Card', () => {
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

  it('Check the computed properties - default', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = mount(ToRegisterCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isErrored).toBeFalsy();
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();

    expect(wrapper.vm.formatted_date).toBeFalsy();

    expect(wrapper.vm.no_orient).toHaveLength(0);
    expect(wrapper.vm.orient_after).toHaveLength(0);
    expect(wrapper.vm.iss_before).toHaveLength(1);
    expect(wrapper.vm.iss_after).toHaveLength(0);
    expect(wrapper.vm.measles_before).toHaveLength(1);
    expect(wrapper.vm.measles_after).toHaveLength(0);
    expect(wrapper.vm.orient_before).toHaveLength(1);
  });

  it('Check the computed properties - international', async () => {
    axios.get.mockResolvedValue({data: interNotices});
    const wrapper = mount(ToRegisterCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isErrored).toBeFalsy();
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();

    expect(wrapper.vm.formatted_date).toBeFalsy();

    expect(wrapper.vm.no_orient).toHaveLength(0);
    expect(wrapper.vm.orient_after).toHaveLength(1);
    expect(wrapper.vm.iss_before).toHaveLength(0);
    expect(wrapper.vm.iss_after).toHaveLength(1);
    expect(wrapper.vm.measles_before).toHaveLength(0);
    expect(wrapper.vm.measles_after).toHaveLength(1);
    expect(wrapper.vm.orient_before).toHaveLength(0);
  });

  it('Check the computed properties - bothell', async () => {
    axios.get.mockResolvedValue({data: bothellNotices});
    const wrapper = mount(ToRegisterCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isErrored).toBeFalsy();
    expect(wrapper.vm.hasRegisterNotices).toBeTruthy();

    expect(wrapper.vm.formatted_date).toBe('Mon, Apr 1');

    expect(wrapper.vm.no_orient).toHaveLength(1);
    expect(wrapper.vm.orient_after).toHaveLength(0);
    expect(wrapper.vm.iss_before).toHaveLength(0);
    expect(wrapper.vm.iss_after).toHaveLength(0);
    expect(wrapper.vm.measles_before).toHaveLength(0);
    expect(wrapper.vm.measles_after).toHaveLength(0);
    expect(wrapper.vm.orient_before).toHaveLength(0);
  });
});
