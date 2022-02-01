import axios from 'axios';
import Vuex from 'vuex';

import {createLocalVue} from '../helper';
import {statusOptions} from '../../vuex/store/model_builder';
import academic_events from '../../vuex/store/academic_events';
import {expectAction} from '../helper';

import mockEventFaculty20210701 from
  '../mock_data/academic_events/acad_events_faulty.json';
import mockEventsStud20210928 from
  '../mock_data/academic_events/acad_events_stud.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Academics Events model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        academic_events,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue(
      {data: mockEventsStud20210928, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(academic_events.actions.fetch, null, academic_events.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockEventsStud20210928},
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
      academic_events.actions.fetch, null, academic_events.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - faculty 20210701', () => {
    axios.get.mockResolvedValue(
        {data: mockEventFaculty20210701, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      academic_events.actions.fetch, null, academic_events.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockEventFaculty20210701},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

  it ('Check postProcess - student 20210928', () => {
    axios.get.mockResolvedValue(
      {data: mockEventsStud20210928, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      academic_events.actions.fetch, null, academic_events.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockEventsStud20210928},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

});
