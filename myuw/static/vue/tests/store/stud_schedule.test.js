import axios from 'axios';
import Vuex from 'vuex';

import {createLocalVue} from '../helper';
import {statusOptions} from '../../vuex/store/model_builder';
import stud_schedule, { postProcess } from '../../vuex/store/schedule/student';
import {expectAction} from '../helper';

import mockCoursesJaverage2013Spring from
  '../mock_data/stud_schedule/javerage2013Spring.json';
import mockCoursesJeos2013Spring from
  '../mock_data/stud_schedule/jeos2013Spring.json';
import mockCoursesJeos2013SummerB from
  '../mock_data/stud_schedule/jeos2013SummerB.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Stud Course model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'stud_schedule': stud_schedule,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue(
      {data: mockCoursesJaverage2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(stud_schedule.actions.fetch, null, stud_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockCoursesJaverage2013Spring},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      stud_schedule.actions.fetch, null, stud_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - javerage 2013 spring', () => {
    axios.get.mockResolvedValue(
        {data: mockCoursesJaverage2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      stud_schedule.actions.fetch, null, stud_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockCoursesJaverage2013Spring},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

  it ('Check postProcess - jeos 2013 spring', () => {
    axios.get.mockResolvedValue(
      {data: mockCoursesJeos2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      stud_schedule.actions.fetch, null, stud_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockCoursesJeos2013Spring},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });
});
