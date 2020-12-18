import axios from 'axios';
import Vuex from 'vuex';
import {createLocalVue} from '@vue/test-utils';
import {statusOptions} from '../vuex/store/model_builder';
import classlist from '../vuex/store/classlist';
import {expectAction} from './helper';

import mockJointPols306A from
  './mock_data/classlist/2013-autumn-POLS-306-A.json';
import mockBillEss102A from
  './mock_data/classlist/2013-spring-ESS-102-A.json';

const localVue = createLocalVue();
localVue.use(Vuex);
jest.mock('axios');

describe('Classlist Data', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'classlist': classlist,
      },
      state: {
        user: {
          netid:"bill",
          affiliations: {
            instructor: true,
          }
        },
        sectionLabel: "2013,spring,ESS,102/A",
      }
    });
  });

  it('Check status on fetch success', async () => {
    axios.get.mockResolvedValue(
      {data: mockBillEss102A, status: 200}
    );
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      classlist.actions.fetch, "2013,spring,ESS,102/A",
      classlist.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockBillEss102A},
        {type: 'setStatus', payload: statusOptions[0]},
      ]);
  });

  it('Check status on fetch failure', () => {
    axios.get.mockResolvedValue(
      Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(
      classlist.actions.fetch, null, classlist.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - billjoint POLS', async () => {
    axios.get.mockResolvedValue(
        {data: mockJointPols306A, status: 200}
    );
    store.dispatch('classlist/fetch', '2013,autumn,POL S,306/A');
    await new Promise((r) => setTimeout(r, 30));
    expect(
      store.getters['classlist/isReadyTagged']('2013,autumn,POL S,306/A')
      ).toBeTruthy();

    expect(store.state.classlist.value).toBeDefined();
    expect(store.state.classlist.value['2013,autumn,POL S,306/A']).toBeDefined();
    const section = store.state.classlist.value['2013,autumn,POL S,306/A'].sections[0];
    expect(section.registrations).toHaveLength(7);

    expect(section.registrations[0].netid).toBe('javg005');
    expect(section.registrations[1].netid).toBe('javg004');
    expect(section.registrations[2].netid).toBe('javg016');
    expect(section.registrations[3].netid).toBe('javg006');
    expect(section.registrations[4].netid).toBe('javg001');
    expect(section.registrations[5].netid).toBe('javg002');
    expect(section.registrations[6].netid).toBe('javg003');
  });
});
