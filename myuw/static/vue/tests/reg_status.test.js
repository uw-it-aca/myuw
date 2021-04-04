import axios from 'axios';
import {mount} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import RegStatus from '../components/home/registration/status.vue';
import notices from '../vuex/store/notices';
import oquarter from '../vuex/store/oquarter';
import profile from '../vuex/store/profile';
import myplan from '../vuex/store/myplan';

import mockNotices from './mock_data/notice/javerage.json';
import myPlanSpring from './mock_data/myplan/spring.json';
import myPlanSummer from './mock_data/myplan/summer.json';
import oQuarterSpring from './mock_data/oquarter/spring.json';
import oQuarterAutumn from './mock_data/oquarter/autumn.json';
import profileJavg001 from './mock_data/profile/javg001.json';
import profileJinter from './mock_data/profile/jinter.json';

import {
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Quicklinks/Link', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
        oquarter,
        profile,
        myplan
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        },
        cardDisplayDates: {
          is_after_start_of_registration_display_period: true,
          is_before_end_of_registration_display_period: true,
          is_after_start_of_summer_reg_display_periodA: false,
          is_after_start_of_summer_reg_display_period1: false,
          myplan_peak_load: false,
        }
      }
    });
  });

  it('Basic Mount', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/oquarters/': oQuarterSpring,
        '/api/v1/profile/': profileJinter,
        '/api/v1/myplan/2013/Spring': myPlanSpring,
      };

      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(RegStatus, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.vm.year).toEqual(2013);
    expect(wrapper.vm.quarter).toEqual('Spring');
    expect(wrapper.vm.terms).toEqual([]);
    expect(wrapper.vm.isAfterStartOfRegistrationDisplayPeriod).toBe(true);
    expect(wrapper.vm.isBeforeEndOfRegistrationDisplayPeriod).toBe(true);
    expect(wrapper.vm.isAfterStartOfSummerRegDisplayPeriodA).toBe(false);
    expect(wrapper.vm.shouldDisplayAtAll).toBe(true);
    expect(wrapper.vm.nextTermHasReg).toBe(false);
  });
});
