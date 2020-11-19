import axios from 'axios';
import dayjs from 'dayjs';
import {mount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import InstructorCourseSummery from
  '../components/home/inst_course_summary/summary.vue';
// import {statusOptions} from '../vuex/store/model_builder';
// import {expectAction} from './helper';
import inst_schedule from '../vuex/store/inst_schedule';

import mockBill2013Summer from
  './mock_data/inst_schedule/bill2013summer.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);

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
          firstDay: "Apr 01 2013 00:00:00 GMT-0700",
        },
        nextTerm: {
          year: 2013,
          quarter: 'summer',
        }
      }
    });
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
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.find('h3').text()).toEqual(
      'Spring 2013 Teaching Schedule');
  });

  it('Check fetch 2013,summer - success', () => {
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

  it('Check status changes on fetch - failure', () => {
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

});
