import axios from 'axios';
import Vuex from 'vuex';

import {createLocalVue} from '../helper';
import {statusOptions} from '../../vuex/store/model_builder';
import category_links from '../../vuex/store/category_links';
import {expectAction} from '../helper';

import mockCalLinks from
  '../mock_data/category_links/calendar.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Category Links model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        category_links,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue(
      {data: mockCalLinks, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(category_links.actions.fetch, null, category_links.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockCalLinks},
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
      category_links.actions.fetch, null, category_links.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - student 20210928', () => {
    axios.get.mockResolvedValue(
      {data: mockCalLinks, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      category_links.actions.fetch, null, category_links.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockCalLinks},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

});
