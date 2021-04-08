import axios from 'axios';
import courses from '../mixins/courses';

import {mount} from '@vue/test-utils';

import Vuex from 'vuex';

import inst_schedule from '../vuex/store/schedule/instructor';
import {createLocalVue} from './helper';

import UwCard from '../components/_templates/card.vue';
import InstructorCourseSummery from
  '../components/home/inst_course_summary/summary.vue';

import mockBill2013Summer from
  './mock_data/inst_schedule/bill2013summer.json';
import mockBillpce2013Summer from
  './mock_data/inst_schedule/billpce2013summer.json';
import mockBillsea2013Spring from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockNoCourse2013Summer from
  './mock_data/inst_schedule/2013summer.json';

const localVue = createLocalVue(Vuex);
localVue.mixin(courses);

jest.mock('axios');

describe('Instructor Teaching Summary', () => {
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

  it('Verify current quarter summary card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/instructor_schedule/current': mockBillsea2013Spring,
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
});
