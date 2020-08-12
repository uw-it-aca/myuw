import axios from 'axios';
import {testAction} from './helper';
import {statusOptions} from '../store/model_builder';
import hfs from '../store/hfs';
import mockRes from './mock_data/hfs.json'

jest.mock('axios');

describe('Library model', () => {
  it('Check status changes on fetch - success', done => {
    axios.get.mockResolvedValue({data: mockRes});
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    testAction(hfs.actions.fetch, null, hfs.state, getters, [
      { type: 'setStatus', payload: statusOptions[1]},
      { type: 'setValue', payload: mockRes},
      { type: 'setStatus', payload: statusOptions[0]},
    ], done);
  });

  it('Check status changes on fetch - failure', done => {
    axios.get.mockResolvedValue(Promise.reject());
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    testAction(hfs.actions.fetch, null, hfs.state, getters, [
      { type: 'setStatus', payload: statusOptions[1]},
      { type: 'setStatus', payload: statusOptions[2]},
    ], done);
  });
});