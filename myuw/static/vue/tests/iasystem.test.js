import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import {expectAction} from './helper';
import {statusOptions} from '../vuex/store/model_builder';
import iasystem from '../vuex/store/iasystem';

import mockJaverage2013Spring from
  './mock_data/iasystem/javerage2013Spring.json';

jest.mock('axios');

describe('Instructor Evaluation model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'iasystem': iasystem,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue(
      {data: mockJaverage2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      iasystem.actions.fetch, null, iasystem.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockJaverage2013Spring},
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
      iasystem.actions.fetch, null, iasystem.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - javerage 2013 spring', () => {
    axios.get.mockResolvedValue(
        {data: mockJaverage2013Spring, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      iasystem.actions.fetch, null, iasystem.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockJaverage2013Spring},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });
});
