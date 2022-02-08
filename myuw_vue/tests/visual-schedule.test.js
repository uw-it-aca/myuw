import axios from 'axios';

import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import visual_schedule from '../vuex/store/schedule/visual';

import CourseSection from '../components/_common/visual_schedule/course-section.vue';
import ScheduleTab from '../components/_common/visual_schedule/schedule-tab.vue';
import VisualSchedule from '../components/_common/visual_schedule/schedule.vue';
import UwTabs from '../components/_templates/tabs/tabs.vue';
import UwTab from '../components/_templates/tabs/button.vue';

import mockScheduleBill from './mock_data/schedule/muwm-5071-bill2013spring.json';
import mockScheduleBillsea2020 from './mock_data/schedule/billsea2020.json';
import mockScheduleJaverage from './mock_data/schedule/muwm-5071-javerage2013spring.json';
import mockScheduleJaverageSummer from './mock_data/schedule/javerageSummer2013.json';
import mockScheduleJeos from './mock_data/schedule/jeos2013.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Vue SFC Tests', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'visual_schedule': visual_schedule,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        },
        termData: {
          quarter: 'summer',
          year: 2013,
        },
        cardDisplayDates: {
          comparison_date: new Date('Mon Apr 1 2013 00:00:00 GMT-0700 (Pacific Daylight Time)'),
        }
      }
    });
  });

  it('Not student nor instructor - not create the card', async() => {
    store.state.user.affiliations.student = false;
    axios.get.mockRejectedValue({response: {status: 404}});
    const wrapper = mount(VisualSchedule, {store, localVue});
    expect(wrapper.vm.showCard).toBe(false);
  });

  it ('Check Mount - javerage', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJaverage, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.termLabel).toBe("current");
    const termData = wrapper.vm.allSchedules["current"].term;
    console.log(wrapper.vm.allSchedules["current"]);
    expect(wrapper.vm.termName).toBe("Spring 2013");
    expect(wrapper.vm.activePeriod.title).toBe("Apr 01 - Jun 07");
    expect(wrapper.vm.periods[0].title).toBe("Apr 01 - Jun 07");
    expect(wrapper.vm.periods[1].title).toBe("finals");
    expect(wrapper.vm.allMeetings).toHaveLength(12);
    expect(wrapper.findComponent(UwTabs).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwTab)).toHaveLength(2);
    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(2);
    expect(wrapper.find('h2').exists()).toBeTruthy();
    expect(wrapper.find('h2').text()).toMatch("Spring 2013 Schedule");
    expect(wrapper.findAll('button[role=tab]').at(0).text()).toBe("Apr 01 - Jun 07");
    expect(wrapper.findAll('button[role=tab]').at(1).text()).toBe("finals");
  });

  it ('Check Mount - javerage summer', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJaverageSummer, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.vm.termName).toBe("Summer 2013 A-Term");
    expect(wrapper.vm.periods[0].title).toBe("Jun 24 - Jul 19");
    expect(wrapper.vm.periods[1].title).toBe("Jul 22 - Jul 24");
    expect(wrapper.vm.allMeetings).toHaveLength(4);
    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(2);
    expect(wrapper.findAllComponents(UwTab)).toHaveLength(2);
  }); 

  it ('Check Mount - jeos', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.vm.termName).toBe("Spring 2013");
    expect(wrapper.vm.periods[0].title).toBe("Apr 01 - Apr 05");
    expect(wrapper.vm.periods[1].title).toBe("Apr 07 - May 03");
    expect(wrapper.vm.periods[2].title).toBe("May 05 - Jun 15");
    expect(wrapper.vm.periods[3].title).toBe("Jun 17 - Jul 06");
    expect(wrapper.vm.periods[4].title).toBe("finals");
    expect(wrapper.vm.periods[0].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[1].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[2].eosData).toHaveLength(1);
    expect(wrapper.vm.periods[3].eosData).toHaveLength(0);
    expect(wrapper.vm.periods[4].eosData).toHaveLength(1);
    expect(wrapper.findAllComponents(ScheduleTab)).toHaveLength(5);
    expect(wrapper.findAll('button[role=tab]').at(0).text()).toBe("Apr 01 - Apr 05");
    expect(wrapper.findAll('button[role=tab]').at(1).text()).toBe("Apr 07 - May 03");
    expect(wrapper.findAll('button[role=tab]').at(2).text()).toBe("May 05 - Jun 15");
    expect(wrapper.findAll('button[role=tab]').at(3).text()).toBe("Jun 17 - Jul 06");
    expect(wrapper.findAll('button[role=tab]').at(4).text()).toBe("finals");
  });

  it ('Check Overlapping classes', async () => {
    store.state.user.affiliations.student = false;
    store.state.user.affiliations.instructor = true;
    axios.get.mockResolvedValue({data: mockScheduleBill, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.vm.termName).toBe("Spring 2013");
    expect(wrapper.vm.periods[0].title).toBe("Apr 01 - Jun 07");
    expect(wrapper.vm.periods[1].title).toBe("finals");
    const wrapper1 = mount(CourseSection, 
      {
        store, localVue, propsData: {
        'meetingData': wrapper.vm.meeting,
        'term': wrapper.vm.getTermData,
      }});
    expect(wrapper1.ariaLabel).tobe("Meeting time: Monday, 8:30am-9:20am");
    expect(wrapper1.sectionTitle).tobe("TRAIN 101 A");
    expect(wrapper1.sectionUrl).tobe("/teaching/2013,spring#TRAIN-101-A");
    expect(wrapper1.meetingLocation).tobe("Room TBD");
  });

  it ('jeos - activePeriod', async () => {
    axios.get.mockResolvedValue({data: mockScheduleJeos, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.termName).toBe("Spring 2013");
    expect(wrapper.vm.periods[0].title).toBe("Apr 01 - Apr 05");
    expect(wrapper.vm.periods[1].title).toBe("Apr 07 - May 03");
    expect(wrapper.vm.periods[2].title).toBe("May 05 - Jun 15");
    expect(wrapper.vm.periods[3].title).toBe("Jun 17 - Jul 06");
    expect(wrapper.vm.periods[4].title).toBe("finals");

    store.state.cardDisplayDates.comparison_date = new Date('Sat Apr 5 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(0);
    
    store.state.cardDisplayDates.comparison_date = new Date('Sat Apr 6 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.cardDisplayDates.comparison_date = new Date('Sun Apr 7 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.cardDisplayDates.comparison_date = new Date('Fri May 3 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(1);

    store.state.cardDisplayDates.comparison_date = new Date('Sat May 4 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(2);

    store.state.cardDisplayDates.comparison_date = new Date('Sun May 5 2013 00:00:00 GMT-0700 (Pacific Daylight Time)');
    expect(wrapper.vm.activePeriod.id).toEqual(2);
  });
});
