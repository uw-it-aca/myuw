import axios from 'axios';
import {mount} from '@vue/test-utils';
import {createLocalVue, expectAction} from './helper';
import {statusOptions} from '../vuex/store/model_builder';
import Vuex from 'vuex';
import Courses from '../vuex/store/schedule/student';
import GradesCard from '../components/_common/grades.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

import {
  faExclamationTriangle,
  faLocationArrow,
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';

import mockCourses from './mock_data/courses.json';

const localVue = createLocalVue(Vuex);

library.add(faExclamationTriangle);
library.add(faLocationArrow);
library.add(faSquareFull);

localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Courses Store', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'stud_schedule': Courses,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockCourses, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(Courses.actions.fetch, null, Courses.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockCourses},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(Courses.actions.fetch, null, Courses.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });
});

describe('Events Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'stud_schedule': Courses,
      },
      state: {
        cardDisplayDates: {
            is_after_7d_before_last_instruction: true,
            is_after_grade_submission_deadline: false,
            is_after_last_day_of_classes: true,
            is_after_start_of_registration_display_period: true,
            is_after_start_of_summer_reg_display_period1: false,
            is_after_start_of_summer_reg_display_periodA: false,
            is_before_eof_7days_of_term: false,
            is_before_end_of_finals_week: false,
            is_before_end_of_registration_display_period: true,
            is_before_end_of_summer_reg_display_periodA: false,
            is_before_end_of_summer_reg_display_period1: false,
            is_before_first_day_of_term: false,
            is_before_last_day_of_classes: false,
            myplan_peak_load: false,
            reg_period1_started: true,
            is_summer: false,
            is_after_summer_b: false,
            in_coursevel_fetch_window: true,
            comparison_date: "2013-06-15T00:00:01",
            current_summer_term: "2013,summer",
            last_term: "2013,winter",
        }
      }
    });
  });

  it('Basic Render - 1', async () => {
    axios.get.mockResolvedValue({data: mockCourses, status: 200});
    const wrapper = mount(GradesCard, {store, localVue});
  
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h2').text()).toEqual('Final Grades');
  });

  it('Basic Render - 2', async () => {
    axios.get.mockResolvedValue({data: mockCourses, status: 200});

    store.state.cardDisplayDates = {
      is_after_7d_before_last_instruction: true,
      is_after_grade_submission_deadline: false,
      is_after_last_day_of_classes: true,
      is_after_start_of_registration_display_period: false,
      is_after_start_of_summer_reg_display_period1: false,
      is_after_start_of_summer_reg_display_periodA: false,
      is_before_eof_7days_of_term: false,
      is_before_end_of_finals_week: false,
      is_before_end_of_registration_display_period: false,
      is_before_end_of_summer_reg_display_periodA: false,
      is_before_end_of_summer_reg_display_period1: false,
      is_before_first_day_of_term: false,
      is_before_last_day_of_classes: false,
      myplan_peak_load: false,
      reg_period1_started: false,
      is_summer: false,
      is_after_summer_b: false,
      in_coursevel_fetch_window: true,
      comparison_date: "2013-12-15T00:00:01",
      current_summer_term: "2013,summer",
      last_term: "2013,summer"
    }
    const wrapper = mount(GradesCard, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h2').text()).toEqual('Final Grades');
  });

  it('Basic Render - 3', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = mount(GradesCard, {store, localVue});

    expect(wrapper.find('h2').exists()).toBe(false);
  });

  it('toFriendlyDate', () => {
    axios.get.mockResolvedValue({data: mockCourses, status: 200});
    const wrapper = mount(GradesCard, {store, localVue});

    expect(
      wrapper.vm.toFriendlyDate('2020-08-24')
    ).toEqual('Mon, Aug 24');

    expect(
      wrapper.vm.toFriendlyDate(undefined)
    ).toEqual('');
    expect(
      wrapper.vm.toFriendlyDate('')
    ).toEqual('');
  });
});
