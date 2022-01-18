import axios from 'axios';
import dayjs from 'dayjs';

import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import visual_schedule from '../../vuex/store/schedule/visual';
import {statusOptions} from '../../vuex/store/model_builder';
import {createLocalVue, expectAction} from '../helper';

import ScheduleTab from '../../components/_common/visual_schedule/schedule-tab.vue';
import VisualSchedule from '../../components/_common/visual_schedule/schedule.vue';

import mockScheduleBill from '../mock_data/schedule/bill2013.json';
import mockScheduleBillsea2020 from '../mock_data/schedule/billsea2020.json';
import mockScheduleJaverage from '../mock_data/schedule/javerage2013.json';
import mockScheduleJaverageSummer from '../mock_data/schedule/javerageSummer2013.json';
import mockScheduleJeos from '../mock_data/schedule/jeos2013.json';
import mockScheduleMuwm5000 from '../mock_data/schedule/2021-aut-muwm-5000.json';
import mockScheduleMuwm5001 from '../mock_data/schedule/2021-aut-muwm-5001.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Schedule Model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'visual_schedule': visual_schedule,
      },
    });
  });

  it ('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleBill},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });

  // Checks if the postProcess method can process data without failing
  it ('Check can process - bill', () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleBill},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it ('Check can process - billsea 2020', () => {
    axios.get.mockResolvedValue({data: mockScheduleBillsea2020, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleBillsea2020},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it ('Check can process - javerage', () => {
    axios.get.mockResolvedValue({data: mockScheduleJaverage, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleJaverage},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it ('Check can process - jeos', () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(visual_schedule.actions.fetch, null, visual_schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleJeos},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it ('Check earliest and latest meeting times', async () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    store.dispatch('visual_schedule/fetch', 'testCurrent');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(store.getters['visual_schedule/isReadyTagged']('testCurrent')).toBeTruthy();

    expect(store.state.visual_schedule.value).toBeDefined();
    expect(store.state.visual_schedule.value.testCurrent).toBeDefined();
    expect(store.state.visual_schedule.value.testCurrent.periods).toHaveLength(2);

    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].earliestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].earliestMeetingTime.format('hh:mm A')
    ).toBe("08:30 AM");

    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].latestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].latestMeetingTime.format('hh:mm A')
    ).toBe("06:20 PM");

    expect(
      store.state.visual_schedule.value.testCurrent.periods[1].earliestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.visual_schedule.value.testCurrent.periods[1].earliestMeetingTime.format('hh:mm A')
    ).toBe("08:30 AM");

    expect(
      store.state.visual_schedule.value.testCurrent.periods[1].latestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.visual_schedule.value.testCurrent.periods[1].latestMeetingTime.format('hh:mm A')
    ).toBe("04:20 PM");
  });

  it ('Check eos data', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    store.dispatch('visual_schedule/fetch', 'testCurrent');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(store.getters['visual_schedule/isReadyTagged']('testCurrent')).toBeTruthy();

    expect(store.state.visual_schedule.value).toBeDefined();
    expect(store.state.visual_schedule.value.testCurrent).toBeDefined();
    expect(store.state.visual_schedule.value.testCurrent.periods).toHaveLength(5);

    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].eosData
    ).toHaveLength(1);
    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].eosData[0].curriculum_abbr
    ).toBe("BIGDATA");
    expect(
      store.state.visual_schedule.value.testCurrent.periods[0].eosData[0].meetings
    ).toHaveLength(3);
  });

  it ('Check postProcess - muwm-5000', async () => {
    axios.get.mockResolvedValue({data: mockScheduleMuwm5000, status: 200});
    store.dispatch('visual_schedule/fetch', 'current');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(store.getters['visual_schedule/isReadyTagged']('current')).toBeTruthy();

    expect(store.state.visual_schedule.value).toBeDefined();
    expect(store.state.visual_schedule.value.current).toBeDefined();
    const scheduleData = store.state.visual_schedule.value.current;
    expect(store.state.visual_schedule.value.current.periods).toHaveLength(3);
    const period1 = store.state.visual_schedule.value.current.periods[0];
    expect(period1.eosData).toHaveLength(0);
  });

  it ('Check postProcess - muwm-5001', async () => {
    axios.get.mockResolvedValue({data: mockScheduleMuwm5001, status: 200});
    store.dispatch('visual_schedule/fetch', 'current');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(store.getters['visual_schedule/isReadyTagged']('current')).toBeTruthy();

    expect(store.state.visual_schedule.value).toBeDefined();
    expect(store.state.visual_schedule.value.current).toBeDefined();
    const scheduleData = store.state.visual_schedule.value.current;
    expect(store.state.visual_schedule.value.current.periods).toHaveLength(3);
    const finalsPeriod = store.state.visual_schedule.value.current.periods[2];
    expect(finalsPeriod.daySlots.saturday).toBeDefined();
  });
});
