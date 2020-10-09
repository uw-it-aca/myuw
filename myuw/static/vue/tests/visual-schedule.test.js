import axios from 'axios';
import dayjs from 'dayjs';

import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import schedule from '../vuex/store/schedule';
import {statusOptions} from '../vuex/store/model_builder';
import {expectAction} from './helper';

import CourseSection from '../components/_common/schedule/course-section.vue';
import ScheduleTab from '../components/_common/schedule/schedule-tab.vue';
import VisualSchedule from '../components/_common/schedule/visual-schedule.vue';

import mockScheduleBill from './mock_data/schedule/bill2013.json';
import mockScheduleBillsea2020 from './mock_data/schedule/billsea2020.json';
import mockScheduleJaverage from './mock_data/schedule/javerage2013.json';
import mockScheduleJaverageSummer from './mock_data/schedule/javerageSummer2013.json';
import mockScheduleJeos from './mock_data/schedule/jeos2013.json';

const localVue = createLocalVue();

jest.mock('axios');

describe('Schedule Model', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'schedule': schedule,
      },
    });
  });

  it ('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };

    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
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
    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
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

    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
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

    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
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

    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
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

    return expectAction(schedule.actions.fetch, null, schedule.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockScheduleJeos},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it ('Check earliest and latest meeting times', async () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    store.dispatch('schedule/fetch', 'testCurrent');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(store.getters['schedule/isReadyTagged']('testCurrent')).toBeTruthy();

    expect(store.state.schedule.value).toBeDefined();
    expect(store.state.schedule.value.testCurrent).toBeDefined();
    expect(store.state.schedule.value.testCurrent.periods).toHaveLength(2);

    expect(
      store.state.schedule.value.testCurrent.periods[0].earliestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.schedule.value.testCurrent.periods[0].earliestMeetingTime.format('hh:mm A')
    ).toBe("08:30 AM");

    expect(
      store.state.schedule.value.testCurrent.periods[0].latestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.schedule.value.testCurrent.periods[0].latestMeetingTime.format('hh:mm A')
    ).toBe("06:20 PM");

    expect(
      store.state.schedule.value.testCurrent.periods[1].earliestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.schedule.value.testCurrent.periods[1].earliestMeetingTime.format('hh:mm A')
    ).toBe("08:30 AM");

    expect(
      store.state.schedule.value.testCurrent.periods[1].latestMeetingTime
    ).toBeInstanceOf(dayjs);
    expect(
      store.state.schedule.value.testCurrent.periods[1].latestMeetingTime.format('hh:mm A')
    ).toBe("04:20 PM");
  });

  it ('Check eos data', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    store.dispatch('schedule/fetch', 'testCurrent');

    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(store.getters['schedule/isReadyTagged']('testCurrent')).toBeTruthy();

    expect(store.state.schedule.value).toBeDefined();
    expect(store.state.schedule.value.testCurrent).toBeDefined();
    expect(store.state.schedule.value.testCurrent.periods).toHaveLength(6);

    expect(
      store.state.schedule.value.testCurrent.periods[0].eosData
    ).toHaveLength(1);
    expect(
      store.state.schedule.value.testCurrent.periods[0].eosData[0].curriculum_abbr
    ).toBe("BIGDATA");
    expect(
      store.state.schedule.value.testCurrent.periods[0].eosData[0].meetings
    ).toHaveLength(3);
  });
});

describe('Vue SFC Tests', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'schedule': schedule,
      },
      state: {
        user: {
          netid: 'test',
        },
        termData: {
          quarter: 'summer',
          year: 2013,
          todayDate: new Date('Mon Apr 1 2013 00:00:00 GMT-0700 (Pacific Daylight Time)'),
        }
      }
    });
  });

  it ('Check Mount - javerage', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJaverage, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').exists()).toBeTruthy();
    expect(wrapper.find('h3').text()).toMatch("Spring 2013 Schedule");
    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(2);

    expect(wrapper.findAll('a[role=tab]').at(0).text()).toBe("Apr 01 - Jun 07");
    expect(wrapper.findAll('a[role=tab]').at(1).text()).toBe("finals");
  });

  it ('Check Mount - javerage summer', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJaverageSummer, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').exists()).toBeTruthy();
    expect(wrapper.find('h3').text()).toMatch("Summer 2013 A-Term Schedule");
    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(2);

    expect(wrapper.findAll('a[role=tab]').at(0).text()).toBe("Jun 24 - Jul 19");
    expect(wrapper.findAll('a[role=tab]').at(1).text()).toBe("Jul 22 - Jul 24");
  }); 

  it ('Check Mount - jeos', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').exists()).toBeTruthy();
    expect(wrapper.find('h3').text()).toMatch("Spring 2013 Schedule");

    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(6);
    expect(wrapper.findAll('a[role=tab]').at(0).text()).toBe("Apr 01 - Apr 05");
    expect(wrapper.findAll('a[role=tab]').at(1).text()).toBe("Apr 07 - May 03");
    expect(wrapper.findAll('a[role=tab]').at(2).text()).toBe("May 05 - May 11");
    expect(wrapper.findAll('a[role=tab]').at(3).text()).toBe("May 13 - Sep 14");
    expect(wrapper.findAll('a[role=tab]').at(4).text()).toBe("Sep 16 - Sep 18");
    expect(wrapper.findAll('a[role=tab]').at(5).text()).toBe("finals");

    expect(wrapper.vm.periods[0].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[1].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[2].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[3].eosData).toHaveLength(0);
    expect(wrapper.vm.periods[4].eosData).toHaveLength(0);
    expect(wrapper.vm.periods[5].eosData).toHaveLength(1);
  });

  it ('Check Overlapping classes', async () => {
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').exists()).toBeTruthy();
    expect(wrapper.find('h3').text()).toMatch("Spring 2013 Schedule");

    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(2);
    expect(wrapper.findAll('a[role=tab]').at(0).text()).toBe("Apr 01 - Jun 07");
    expect(wrapper.findAll('a[role=tab]').at(1).text()).toBe("finals");

    expect(
      wrapper.findAllComponents(ScheduleTab).at(0).vm
        .meetingMap["tuesday"]["08:30 AM"]
    ).toHaveLength(2);

    expect(
      wrapper.findAllComponents(ScheduleTab).at(1).vm
        .meetingMap["monday"]["08:30 AM"]
    ).toHaveLength(2);
  });

  it ('jeos - activePeriod', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').exists()).toBeTruthy();
    expect(wrapper.find('h3').text()).toMatch("Spring 2013 Schedule");

    expect(wrapper.vm.activePeriod.id).toEqual(0);
    
    store.state.termData.todayDate = new Date('Sat Apr 6 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.termData.todayDate = new Date('Sun Apr 7 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.termData.todayDate = new Date('Fri May 3 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.termData.todayDate = new Date('Sat May 4 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(2);

    store.state.termData.todayDate = new Date('Sun May 5 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(2);
  });
});