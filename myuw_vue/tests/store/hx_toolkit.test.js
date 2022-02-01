import axios from 'axios';
import {expectAction} from '../helper';
import {statusOptions} from '../../vuex/store/model_builder';

import hx_toolkit from '../../vuex/store/hx_toolkit';
import mockList from '../mock_data/husky-exp/list.json';

jest.mock('axios');
describe('hx_toolkit model', () => {
  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockList, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(hx_toolkit.actions.fetch, null, hx_toolkit.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockList},
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
