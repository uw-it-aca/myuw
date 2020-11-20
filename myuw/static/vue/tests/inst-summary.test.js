import axios from 'axios';
import dayjs from 'dayjs';
import utils from '../mixins/utils';
import courses from '../mixins/courses';

import {shallowMount, createLocalVue} from '@vue/test-utils';

import Vuex from 'vuex';

import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';

import {statusOptions} from '../vuex/store/model_builder';
import inst_schedule from '../vuex/store/inst_schedule';
import {expectAction} from './helper';

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

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.mixin(courses);
localVue.mixin(utils);
localVue.component('font-awesome-icon', FontAwesomeIcon);

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
        }
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

    const wrapper = shallowMount(InstructorCourseSummery, {store, localVue});
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
      wrapper.find('h3').text()
    ).toEqual('Spring 2013 Teaching Schedule');

  });

  it('Verify no future quarter summary card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
          '/api/v1/instructor_schedule/2013,summer': mockNoCourse2013Summer,
        };
        return Promise.resolve({data: urlData[url], status: 200});
      });

    const wrapper = shallowMount(
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
