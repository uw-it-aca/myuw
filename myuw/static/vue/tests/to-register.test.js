import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import ToRegisterCard from '../components/pages/index/cards/new_student/to-register.vue';

import mockNotices from './mock_data/notices.json';
import interNotices from './mock_data/inter_notices.json';
import bothellNotices from './mock_data/bothell_notices.json';

import {library} from '@fortawesome/fontawesome-svg-core';

import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';

import {
  faCheckCircle,
} from '@fortawesome/free-solid-svg-icons';

import {
  faCircle,
} from '@fortawesome/free-regular-svg-icons';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

library.add(faCircle);
library.add(faCheckCircle);

localVue.component('font-awesome-icon', FontAwesomeIcon);

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
