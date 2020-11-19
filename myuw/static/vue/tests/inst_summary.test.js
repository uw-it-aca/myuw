import axios from 'axios';
import dayjs from 'dayjs';
import courses from '../mixins/courses';

import {mount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import InstructorCourseSummery from
  '../components/home/inst_course_summary/summary.vue';
import {statusOptions} from '../vuex/store/model_builder';
import {expectAction} from './helper';
import inst_schedule from '../vuex/store/inst_schedule';
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

import mockBill2013Summer from
  './mock_data/inst_schedule/bill2013summer.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';

library.add(faExclamationTriangle);
const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);
localVue.mixin(courses);
localVue.component('font-awesome-icon', FontAwesomeIcon);

jest.mock('axios');

describe('Instructor Schedule Summary', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'inst_schedule': inst_schedule,
      },
      state: {
        user: {
          netid:"billsea",
          affiliations: {
            instructor: true,
          }
        },
        termData: {
          year: 2013,
          quarter: 'spring',
        },
        nextTerm: {
          year: 2013,
          quarter: 'summer',
        }
      }
    });
  });

  it('Check status on fetch success', async () => {
    axios.get.mockResolvedValue(
      {data: mockNoCourse2013Summer, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      inst_schedule.actions.fetch, null, inst_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockNoCourse2013Summer},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

  it('Check status on fetch failure', () => {
    axios.get.mockResolvedValue(
      Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      inst_schedule.actions.fetch, null, inst_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - billsea 2013 spring', () => {
    axios.get.mockResolvedValue(
        {data: mockBillsea2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      inst_schedule.actions.fetch, null, inst_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockBillsea2013Spring},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

  it('Basic Mount', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/instructor_schedule/current': mockBillsea2013Spring,
        '/api/v1/instructor_schedule/2013,summer': mockNoCourse2013Summer,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(InstructorCourseSummery, {store, localVue});
    await new Promise((r) => setTimeout(r, 30));

    expect(
      inst_schedule.getters.isReady(
        wrapper.vm.$store.state.inst_schedule),
      ).toBeTruthy();

    expect(
      inst_schedule.getters.isErrored(
        wrapper.vm.$store.state.inst_schedule),
      ).toBeFalsy();

    expect(
      inst_schedule.getters.statusCode(
        wrapper.vm.$store.state.inst_schedule),
      ).toEqual(200);

    expect(
      wrapper.find('h3').text()).toEqual(
        'Spring 2013 Teaching Schedule');
  });

});
