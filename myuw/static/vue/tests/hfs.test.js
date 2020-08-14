import axios from 'axios';
import {expectAction} from './helper';
import {statusOptions} from '../store/model_builder';
import hfs from '../store/hfs';
import mockRes from './mock_data/hfs.json';

jest.mock('axios');

describe('Library model', () => {
  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockRes});
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(hfs.actions.fetch, null, hfs.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockRes},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject(new Error('Test Reject')));
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(hfs.actions.fetch, null, hfs.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });
});
