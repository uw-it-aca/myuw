import axios from 'axios';
import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import visual_schedule from '../vuex/store/schedule/visual';

import ScheduleTab from '../components/_common/visual_schedule/schedule-tab.vue';
import VisualSchedule from '../components/_common/visual_schedule/schedule.vue';
import CourseSection from '../components/_common/visual_schedule/course-section.vue';
import UwTabs from '../components/_templates/tabs/tabs.vue';
import UwTab from '../components/_templates/tabs/button.vue';

import mockScheduleBill5099 from './mock_data/schedule/muwm-5099-bill2013spring.json';
import mockScheduleBill5071 from './mock_data/schedule/muwm-5071-bill2013spring.json';
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
          comparison_date: dayjs("2013-04-05T00:00:01"),
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
    expect(wrapper.vm.tabIndex).toBe(0);
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
    let wrapper = mount(VisualSchedule, {store, localVue});

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

    // test active tab index
    expect(wrapper.vm.tabIndex).toBe(0);

    let today = dayjs("2013-04-06T00:00:01");
    store.state.cardDisplayDates.comparison_date = today;
    wrapper = mount(VisualSchedule, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.tabIndex).toEqual(1);
    expect(wrapper.vm.endOfDay(wrapper.vm.periods[0].end_date)).toEqual(
      dayjs("2013-04-05T23:59:00.000Z"));
    expect(wrapper.vm.formatDate(wrapper.vm.periods[0].end_date)).toEqual(
      "Fri, Apr 5");

    today = dayjs("2013-05-04T00:00:01");
    store.state.cardDisplayDates.comparison_date = today;
    wrapper = mount(VisualSchedule, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.tabIndex).toEqual(2);

    today = dayjs("2013-07-07T00:00:01");
    store.state.cardDisplayDates.comparison_date = today;
    wrapper = mount(VisualSchedule, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.tabIndex).toEqual(4);
  });

  it ('Check Overlapping classes', async () => {
    store.state.user.affiliations.student = false;
    store.state.user.affiliations.instructor = true;
    axios.get.mockResolvedValue({data: mockScheduleBill5071, status: 200});
    const wrapper = mount(VisualSchedule, {store, localVue});

    await new Promise(setImmediate);
    expect(wrapper.vm.termName).toBe("Spring 2013");
    expect(wrapper.vm.periods[0].title).toBe("Apr 01 - Jun 07");
    expect(wrapper.vm.periods[1].title).toBe("finals");
    const tabs = wrapper.findAllComponents(ScheduleTab)
    expect(tabs).toHaveLength(2);
    expect(tabs.at(0).vm.hasOverlappingMeetings).toBe(true)
    expect(tabs.at(1).vm.hasOverlappingMeetings).toBe(false)

    expect(
      wrapper.findAllComponents(ScheduleTab).at(0).vm
        .meetingMap["tuesday"]["08:30 AM"]
    ).toHaveLength(2);

    expect(
       wrapper.findAllComponents(ScheduleTab).at(1).vm
        .meetingMap["monday"]["08:30 AM"]
    ).toHaveLength(1);
    expect(
      wrapper.findAllComponents(ScheduleTab).at(1).vm
        .meetingMap["sunday"]["08:30 AM"]
    ).toHaveLength(1);
  });

  it('Check MUWM-5099 MUWM-5208', async () => {
    store.state.user.affiliations.student = false;
    store.state.user.affiliations.instructor = true;
    axios.get.mockResolvedValue({ data: mockScheduleBill5099, status: 200 });
    const wrapper = mount(VisualSchedule, { store, localVue });

    await new Promise(setImmediate);
    const sections = wrapper.findAllComponents(CourseSection);
    expect(sections.at(0).vm.isFinalsTab).toBe(false);
    expect(sections.at(0).vm.isInPerson).toBe(false);
    expect(sections.at(0).vm.hasBuildingRoom).toBe(false);
    expect(sections.at(0).vm.noLocation).toBe(true);
    expect(sections.at(0).vm.meetingLocation).toBe('Online');
    expect(sections.at(0).vm.ariaMeetingLocation).toBe('Location: Online');
    expect(sections.at(2).vm.isInPerson).toBe(false);
    expect(sections.at(2).vm.hasBuildingRoom).toBe(false);
    expect(sections.at(2).vm.noLocation).toBe(true);
    expect(sections.at(2).vm.finalNoDate).toBe(false);
    expect(sections.at(2).vm.meetingLocation).toBe('Online');
  });
});
