import axios from 'axios';
import courses from '../mixins/courses';

import {mount} from '@vue/test-utils';

import Vuex from 'vuex';

import inst_schedule from '../vuex/store/schedule/instructor';
import notices from '../vuex/store/notices';
import {createLocalVue} from './helper';

import UwCard from '../components/_templates/card.vue';
import InstructorCourseSummery from
  '../components/home/inst_course_summary/summary.vue';
import UwSummerSectionList from
  '../components/home/inst_course_summary/summer-list.vue';
import UwSectionList from
  '../components/home/inst_course_summary/section-list.vue';
import UwCollapsedNotice from
  '../components/_common/collapsed-notice.vue';
import UwCourseMode from
  '../components/_common/course/course-mode/mode.vue';

import mockScheduleBill5099 from 
  './mock_data/inst_schedule/bill2013spr.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';
import mockNotices from
  './mock_data/notice/bill.json';

const localVue = createLocalVue(Vuex);
localVue.mixin(courses);

jest.mock('axios');

describe('Instructor Teaching Summary', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        inst_schedule,
        notices
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
          comparison_date: '2013-05-27T00:00:01',
        },
      }
    });
  });

  it('Verify current quarter summary card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/instructor_schedule/current': mockBillsea2013Spring,
        '/api/v1/notices/': mockNotices,
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });

    const wrapper = mount(InstructorCourseSummery, {store, localVue});
    await new Promise((r) => setTimeout(r, 30));

    expect(
      inst_schedule.getters.isReadyTagged(
        wrapper.vm.$store.state.inst_schedule
      )("current"),
    ).toBeTruthy();

    expect(
      inst_schedule.getters.isErroredTagged(
        wrapper.vm.$store.state.inst_schedule
      )("current"),
    ).toBeFalsy();

    expect(
      inst_schedule.getters.statusCodeTagged(
        wrapper.vm.$store.state.inst_schedule
      )("current"),
    ).toEqual(200);

    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);

    expect(
      wrapper.find('h2').text()
    ).toEqual('Spring 2013 Teaching Schedule');

  });

  it('Verify no future quarter summary card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
          '/api/v1/instructor_schedule/2013,summer': mockNoCourse2013Summer,
          '/api/v1/notices/': mockNotices,
        };
        return Promise.resolve({data: urlData[url], status: 200});
      });

    const wrapper = mount(
      InstructorCourseSummery, {
        store,
        localVue,
        propsData: {
          term: '2013,summer',
        }
      }
    );
    await new Promise((r) => setTimeout(r, 30));

    expect(
      inst_schedule.getters.isReadyTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toBeTruthy();

    expect(
      inst_schedule.getters.isErroredTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toBeFalsy();

    expect(
      inst_schedule.getters.statusCodeTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toEqual(200);

    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Verify Summer quarter summary card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
          '/api/v1/instructor_schedule/2013,summer': mockBillpce2013Summer,
          '/api/v1/notices/': mockNotices,
        };
        return Promise.resolve({data: urlData[url], status: 200});
      });

    const wrapper = mount(
      InstructorCourseSummery, {
        store,
        localVue,
        propsData: {
          term: '2013,summer',
        }
      }
    );
    await new Promise((r) => setTimeout(r, 30));

    expect(
      inst_schedule.getters.isReadyTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toBeTruthy();

    expect(
      inst_schedule.getters.isErroredTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toBe(false);

    expect(
      inst_schedule.getters.statusCodeTagged(
        wrapper.vm.$store.state.inst_schedule
      )("2013,summer"),
    ).toEqual(200);

    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.findComponent(
      UwSummerSectionList).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwSectionList).length).toBe(2);
  });

  it('Check MUWM-5099', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/instructor_schedule/current': mockScheduleBill5099,
        '/api/v1/notices/': mockNotices,
      };
      return Promise.resolve({ data: urlData[url], status: 200 });
    });

    const wrapper = mount(InstructorCourseSummery, { store, localVue });
    await new Promise((r) => setTimeout(r, 30));
    const cmodes = wrapper.findAllComponents(UwCourseMode);
    expect(cmodes.length).toBe(2);
    console.log(cmodes[0]);
    expect(cmodes.at(0).vm.hideInfoLink).toBe(true);
    expect(cmodes.at(0).vm.asyncMsg.length > 0).toBe(true);
    expect(cmodes.at(0).vm.syncMsg.length > 0).toBe(true);
    expect(cmodes.at(0).vm.hybMsg.length > 0).toBe(true);
    expect(cmodes.at(0).vm.inPersonMsg.length > 0).toBe(true);
  });

  it('Check 4072', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/instructor_schedule/current': mockBillsea2013Spring,
        '/api/v1/notices/': mockNotices,
      };
      return Promise.resolve({ data: urlData[url], status: 200 });
    });
    const wrapper = mount(InstructorCourseSummery, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.notices.length).toBe(2);
    expect(wrapper.vm.hasGradingNotices).toBe(true);
    expect(wrapper.vm.gradingNotice).toBeTruthy();
    expect(wrapper.vm.hasClassResAccNotice).toBe(false);
    expect(wrapper.vm.gradingNotice.is_critical).toBe(true);
    expect(wrapper.findAllComponents(UwCollapsedNotice).length).toBe(1);
  });
});
