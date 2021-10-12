import axios from 'axios';

import Vuex from 'vuex';

import advisers from '../../vuex/store/advisers';
import { statusOptions } from '../../vuex/store/model_builder';
import { createLocalVue, expectAction } from '../helper';

import javgAdvisers from '../mock_data/advisers/javerage.json';
import inactiveAdvisers from '../mock_data/advisers/jbot.json';

const localVue = createLocalVue(Vuex);
jest.mock('axios');

describe('Adviser store', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        advisers,
      }
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({ data: javgAdvisers, status: 200 });
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      advisers.actions.fetch, null, advisers.state, getters, [
      { type: 'setStatus', payload: statusOptions[1] },
      { type: 'setValue', payload: javgAdvisers },
      { type: 'setStatus', payload: statusOptions[0] },
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({ response: { status: 404 } }));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      advisers.actions.fetch, null, advisers.state, getters, [
      { type: 'setStatus', payload: statusOptions[1] },
      { type: 'setStatus', payload: statusOptions[2] },
    ]);
  });

  it('Check postProcess - javerage', async () => {
    axios.get.mockResolvedValue({ data: javgAdvisers, status: 200 });
    store.dispatch('advisers/fetch');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(store.getters['advisers/isReady']).toBeTruthy();
    expect(store.state.advisers.value).toBeDefined();
    expect(store.state.advisers.value.length).toBe(5);
    const data = store.state.advisers.value;
    expect(data[0].program).toBe("UAA Advising");
    expect(data[1].program).toBe("OMAD Advising");
    expect(data[2].program).toBe("UW Honors");
    expect(data[3].program).toBe("Robinson Center");
    expect(data[4].program).toBe("Athletics – SAAS");
  });

  it('Check postProcess - Not active', async () => {
    axios.get.mockResolvedValue({ data: inactiveAdvisers, status: 200 });
    store.dispatch('advisers/fetch');
    await new Promise(setImmediate);
    expect(store.getters['advisers/isReady']).toBeTruthy();
    expect(store.state.advisers.value).toBeDefined();
    expect(store.state.advisers.value.length).toBe(0);
  });
});