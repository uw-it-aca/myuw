import axios from 'axios';
import {expectAction} from './helper';
import {statusOptions} from '../store/model_builder';
import library from '../store/library';

jest.mock('axios');

describe('Library model', () => {
  const mockRes = {
    holds_ready: 1,
    fines: 0,
    items_loaned: 1,
    next_due: '2014-05-27T02:00:00+00:00',
  };

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockRes, status: 200});
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(library.actions.fetch, null, library.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockRes},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(library.actions.fetch, null, library.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });
});
