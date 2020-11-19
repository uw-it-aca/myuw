import axios from 'axios';
import dayjs from 'dayjs';
import utils from '../mixins/utils';
import courses from '../mixins/courses';

import createLocalVue from '@vue/test-utils';
import Vuex from 'vuex';

import {statusOptions} from '../vuex/store/model_builder';
import inst_schedule from '../vuex/store/inst_schedule';
import {expectAction} from './helper';

import mockBill2013Summer from
  './mock_data/inst_schedule/bill2013summer.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.mixin(courses);
localVue.mixin(utils);
localVue.component('font-awesome-icon', FontAwesomeIcon);

describe('Instructor Schedule Data', () => {
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
      return Promise.resolve({data: urlData[url], status: 200});
    });
    const wrapper = mount(InstructorCourseSummery, {store, localVue});
    await new Promise((r) => setTimeout(r, 30));

    expect(
      inst_schedule.getters.isReadyTagged(
        wrapper.vm.$store.state.inst_schedule
      )('current'),
    ).toBeTruthy();

    expect(
      inst_schedule.getters.isErroredTagged(
        wrapper.vm.$store.state.inst_schedule
      )('current'),
    ).toBeFalsy();

    expect(
      inst_schedule.getters.statusCodeTagged(
        wrapper.vm.$store.state.inst_schedule
      )('current'),
    ).toEqual(200);

    expect(
      wrapper.find('h3').text()).toEqual(
        'Spring\n      2013 Teaching Schedule');
  });

});
