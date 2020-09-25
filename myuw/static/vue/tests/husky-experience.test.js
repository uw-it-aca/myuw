import axios from 'axios';
import {expectAction} from './helper';
import {statusOptions} from '../store/model_builder';
import hx_toolkit from '../store/hx_toolkit';
import mockRes from './mock_data/husky-experience.html';

jest.mock('axios');

describe('hx_toolkit model', () => {
  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockRes, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(hx_toolkit.actions.fetch, null, hx_toolkit.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockRes},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(hx_toolkit.actions.fetch, null, hx_toolkit.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });
});
