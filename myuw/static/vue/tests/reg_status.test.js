import axios from 'axios';
import {mount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import RegStatus from '../components/home/registration/status.vue';
import notices from '../vuex/store/notices';
import oquarter from '../vuex/store/oquarter';
import profile from '../vuex/store/profile';
import myplan from '../vuex/store/myplan';

import mockNotices from './mock_data/notices.json';
import myPlanSpring from './mock_data/myplan/spring.json';
import myPlanSummer from './mock_data/myplan/summer.json';
import oQuarterSpring from './mock_data/oquarter/spring.json';
import oQuarterAutumn from './mock_data/oquarter/autumn.json';
import profileJavg001 from './mock_data/profile/javg001.json';
import profileJinter from './mock_data/profile/jinter.json';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

const localVue = createLocalVue(Vuex);
localVue.use(BootstrapVue);
localVue.use(Vuex);

library.add(faExclamationTriangle);

localVue.component('font-awesome-icon', FontAwesomeIcon);
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
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.find('h3').text()).toEqual('Registration: Spring 2013');
  });

  // TODO: ADD MORE TEST CASES
});
