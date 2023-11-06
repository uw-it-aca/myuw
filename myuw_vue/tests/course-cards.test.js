import axios from 'axios';
import { createLocalVue } from './helper';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import CourseCards from '../components/_common/course/student/course-cards.vue';
import CourseCard from '../components/_common/course/student/course.vue';
import MeetingInfo from '../components/_common/course/meeting/schedule.vue';
import Instructors from '../components/_common/course/student/instructors.vue';
import Resources from '../components/_common/course/student/resources.vue';
import Textbook from '../components/_common/course/textbook.vue';

import stud_schedule from '../vuex/store/schedule/student';

import courses from '../mixins/courses';
import iasystem from '../vuex/store/iasystem';
import textbooks from '../vuex/store/textbooks';

import mockStudCourses from
  './mock_data/stud_schedule/javerage2013Spring.json';
import mockCourseEval from
  './mock_data/iasystem/javerage2013Spring.json';

const localVue = createLocalVue(Vuex);
localVue.mixin(courses);
jest.mock('axios');

describe('Student Course cards', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        iasystem,
        textbooks,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        },
        termData: {
          year: 2013,
          quarter: "spring",
        },
        cardDisplayDates: {
          is_before_eof_7days_of_term: true,
        }
      }
    });
  });

  it('Verify normal display with javerage', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/schedule/current': mockStudCourses,
        '/api/v1/ias/': mockCourseEval,
      };
      return Promise.resolve({data: urlData[url]});
    });

    let wrapper = mount(CourseCards, {store, localVue,
      propsData: {'term': 'current'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.isCurrentTerm).toBe(true);
    expect(wrapper.vm.quarter).toBe("spring");
    expect(wrapper.vm.student ).toBe(true);
    expect(wrapper.vm.course).toBeTruthy();
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.findAllComponents(CourseCard).length).toBe(5);
    expect(wrapper.findAllComponents(MeetingInfo).length).toBe(5);
    expect(wrapper.findAllComponents(Instructors).length).toBe(3);
    expect(wrapper.findAllComponents(Resources).length).toBe(5);
    const section = wrapper.vm.course.sections[0];
    wrapper = mount(Textbook, {
      store, localVue,
      propsData: { 'term': 'current', 'section': section}
    });
    await new Promise(setImmediate);
    expect(wrapper.vm.termId).toBe("2");
    expect(wrapper.vm.uwtCourse).toBe(false);
    expect(wrapper.vm.textbookPageUrl).toBeTruthy();
    expect(wrapper.vm.uwtTextbookUrl).toBeTruthy();
  });

  it('Hide card if not student', () => {
    store.state.user.affiliations.student = false;
    const wrapper = mount(CourseCards, {store, localVue,
      propsData: {'term': 'current'}});
    expect(wrapper.findComponent(CourseCards).exists()).toBe(true);
    expect(wrapper.findAllComponents(CourseCard).length).toBe(0);
  });

  it('Show error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 543}});
    });
    const wrapper = mount(CourseCards, {store, localVue,
      propsData: {'term': 'current'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
  });
});
