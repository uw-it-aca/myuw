import axios from 'axios';
import Vuex from 'vuex';
import {statusOptions} from '../vuex/store/model_builder';
import inst_schedule from '../vuex/store/schedule/instructor';
import {expectAction, createLocalVue} from './helper';

import mockBill2013Summer from
  './mock_data/inst_schedule/bill2013summer.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';

createLocalVue(Vuex);
jest.mock('axios');

describe('Instructor Schedule Data', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'inst_schedule': inst_schedule,
      },
      state: {
        user: {
          netid:"billsea",
          affiliations: {
            instructor: true,
          }
        },
        termData: {
          year: 2013,
          quarter: 'spring',
        },
        nextTerm: {
          year: 2013,
          quarter: 'summer',
        },
        cardDisplayDates: {
          comparison_date: '2013-04-15T00:00:01',
        },
      }
    });
  });

  it('Check status on fetch success', async () => {
    axios.get.mockResolvedValue(
      {data: mockNoCourse2013Summer, status: 200}
    );

    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(
      inst_schedule.actions.fetch, null, inst_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setValue', payload: mockNoCourse2013Summer},
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
      inst_schedule.actions.fetch, null, inst_schedule.state, getters, [
        {type: 'setStatus', payload: statusOptions[1]},
        {type: 'setStatus', payload: statusOptions[2]},
      ]);
  });

  it ('Check postProcess - billsea 2013 spring', async () => {
    axios.get.mockResolvedValue(
        {data: mockBillsea2013Spring, status: 200}
    );
    store.dispatch('inst_schedule/fetch', 'testCurrent');
    await new Promise((r) => setTimeout(r, 30));
    expect(
      store.getters['inst_schedule/isReadyTagged']('testCurrent')
      ).toBeTruthy();

    expect(store.state.inst_schedule.value).toBeDefined();
    expect(store.state.inst_schedule.value.testCurrent).toBeDefined();
    const sections = store.state.inst_schedule.value.testCurrent.sections;
    expect(sections).toHaveLength(8);
    expect(sections[0].year).toBe(2013);
    expect(sections[0].quarter).toBe('spring');
    expect(sections[0].anchor).toBe('PHYS-122-A');
    expect(sections[0].id).toBe('2013-spring-PHYS-122-A');
    expect(sections[0].href).toBe('2013,spring#PHYS-122-A');
    expect(sections[0].navtarget).toBe('2013,spring,PHYS-122-A');
    expect(sections[0].isPrevTermEnrollment).toBe(false);
  });

  it ('Check postProcess - billpce 2013 summer', async () => {
    axios.get.mockResolvedValue(
        {data: mockBillpce2013Summer, status: 200}
    );
    store.dispatch('inst_schedule/fetch', 'testCurrent');
    await new Promise(setImmediate);
    expect(
      store.getters['inst_schedule/isReadyTagged']('testCurrent')
      ).toBeTruthy();

    expect(store.state.inst_schedule.value).toBeDefined();
    expect(store.state.inst_schedule.value.testCurrent).toBeDefined();
    const sections = store.state.inst_schedule.value.testCurrent.sections;
    expect(sections).toHaveLength(3);
    expect(sections[2].id).toBe("2013-summer-EDIT-120-C");
    expect(sections[2].isPrevTermEnrollment).toBe(false);
  });

});
