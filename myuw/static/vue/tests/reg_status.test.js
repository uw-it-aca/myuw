import axios from 'axios';
import {mount} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import UwCard from '../components/_templates/card.vue';
import RegStatus from '../components/home/registration/status.vue';
import EstRegDate from '../components/home/registration/est-reg-date.vue';
import Holds from '../components/home/registration/holds.vue';
import Myplan from '../components/home/registration/myplan.vue';
import MyplanCourses from '../components/home/registration/myplan-courses.vue';
import Resources from '../components/home/registration/resources.vue';
import FinAids from '../components/_common/finaid.vue';

import notices from '../vuex/store/notices';
import oquarter from '../vuex/store/oquarter';
import profile from '../vuex/store/profile';
import myplan from '../vuex/store/myplan';

import mockNotices from './mock_data/notice/jinter.json';
import myPlanAutumn from './mock_data/myplan/jinter-20130510.json';
import myPlanSpring from './mock_data/myplan/jinter-20130210.json';
import myPlanSummer from './mock_data/myplan/summer.json';
import oQuarterSpring from './mock_data/oquarter/spring.json';
import oQuarterSumAut from './mock_data/oquarter/summer.json';
import profileJavg001 from './mock_data/profile/javg001.json';
import profileJinter from './mock_data/profile/jinter.json';

import {
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Registration Status Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
        oquarter,
        profile,
        myplan
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        },
        cardDisplayDates: {
          is_after_start_of_registration_display_period: true,
          is_before_end_of_registration_display_period: true,
          is_after_start_of_summer_reg_display_periodA: true,
          is_after_start_of_summer_reg_display_period1: false,
          myplan_peak_load: false,
        }
      }
    });
  });

  it('Test normal case1, Jinter 2013 Spring', async () => {
    store.state.cardDisplayDates.is_after_start_of_registration_display_period = false;
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/oquarters/': oQuarterSpring,
        '/api/v1/profile/': profileJinter,
        '/api/v1/myplan/2013/Spring': myPlanSpring,
      };

      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(RegStatus, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.shouldDisplayAtAll).toBe(false);
  });

  it('Test normal case1, Jinter 2013 Spring', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/oquarters/': oQuarterSpring,
        '/api/v1/profile/': profileJinter,
        '/api/v1/myplan/2013/Spring': myPlanSpring,
      };

      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(RegStatus, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.vm.year).toEqual(2013);
    expect(wrapper.vm.quarter).toEqual('Spring');
    expect(wrapper.vm.isAfterStartOfRegistrationDisplayPeriod).toBe(true);
    expect(wrapper.vm.isBeforeEndOfRegistrationDisplayPeriod).toBe(true);
    expect(wrapper.vm.shouldDisplayAtAll).toBe(true);
    expect(wrapper.vm.isSummerReg).toBe(false);
    expect(wrapper.vm.hasRegistration).toBe(false);
    expect(wrapper.vm.finAidNotices.length).toBe(0);
    expect(wrapper.vm.regHoldsNotices.length).toBe(2);
    const myPlanCourses = wrapper.vm.myPlanData.terms[0];
    expect(myPlanCourses.ready_count).toBe(6);
    expect(myPlanCourses.has_ready_courses).toBe(true);
    expect(myPlanCourses.has_sections).toBe(true);
    expect(myPlanCourses.has_unready_courses).toBe(false);
    expect(wrapper.findComponent(Holds).exists()).toBe(true);
    expect(wrapper.findComponent(Myplan).exists()).toBe(true);
    expect(wrapper.findComponent(MyplanCourses).exists()).toBe(true);
    expect(wrapper.findComponent(Resources).exists()).toBe(true);
  });

  it('Test normal case2, Jinter 2013 summer', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/oquarters/': oQuarterSumAut,
        '/api/v1/profile/': profileJinter,
        '/api/v1/myplan/2013/Summer': myPlanSummer,
      };

      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(RegStatus, {store, localVue,
      propsData: {'forQuarter': 'Summer', 'period': 'A'}});
    await new Promise(setImmediate);

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.vm.year).toEqual(2013);
    expect(wrapper.vm.quarter).toBe('Summer');
    expect(wrapper.vm.isAfterStartOfSummerRegDisplayPeriodA).toBe(true);
    expect(wrapper.vm.isAfterStartOfSummerRegDisplayPeriod1).toBe(false);
    expect(wrapper.vm.shouldDisplayAtAll).toBe(true);
    expect(wrapper.vm.isSummerReg).toBe(true);
    expect(wrapper.vm.hasRegistration).toBe(false);
    expect(wrapper.vm.hasDataToDisplay).toBe(1);
    expect(wrapper.vm.summerShouldDisplay).toBe(true);
    expect(wrapper.vm.finAidNotices.length).toBe(1);
    expect(wrapper.vm.regHoldsNotices.length).toBe(2);
    const myPlanCourses = wrapper.vm.myPlanData.terms[0];
    expect(myPlanCourses.ready_count).toBe(2);
    expect(myPlanCourses.has_ready_courses).toBe(true);
    expect(myPlanCourses.has_sections).toBe(true);
    expect(myPlanCourses.has_unready_courses).toBe(true);
    expect(myPlanCourses.unready_count).toBe(1);
    expect(wrapper.findComponent(Myplan).exists()).toBe(true);
    expect(wrapper.findComponent(MyplanCourses).exists()).toBe(true);
    expect(wrapper.findComponent(Resources).exists()).toBe(true);
    expect(wrapper.findComponent(FinAids).exists()).toBe(true);
  });

  it('Test normal case3, Jinter 2013 Autumn', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/oquarters/': oQuarterSumAut,
        '/api/v1/profile/': profileJinter,
        '/api/v1/myplan/2013/Autumn': myPlanAutumn,
      };

      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(RegStatus, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.vm.loaded).toBeTruthy();
    expect(wrapper.vm.year).toEqual(2013);
    expect(wrapper.vm.quarter).toEqual('Autumn');
    expect(wrapper.vm.shouldDisplayAtAll).toBe(true);
    expect(wrapper.vm.hasRegistration).toBe(false);
    expect(wrapper.vm.hasDataToDisplay).toBeTruthy();
    expect(wrapper.vm.finAidNotices.length).toBe(0);
    expect(wrapper.vm.pendingMajors.length).toBe(1);
    expect(wrapper.vm.pendingMinors.length).toBe(1);
    expect(wrapper.vm.regHoldsNotices.length).toBe(2);
    expect(wrapper.vm.estRegDateNotices.length).toBe(1);
    expect(wrapper.vm.estRegData.estRegDate).toBe("Fri, May 10");  // MUWM-5034
    const myPlanCourses = wrapper.vm.myPlanData.terms[0];
    expect(myPlanCourses.ready_count).toBe(0);
    expect(myPlanCourses.has_ready_courses).toBe(false);
    expect(myPlanCourses.has_unready_courses).toBe(true);
    expect(myPlanCourses.unready_count).toBe(5);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.findComponent(EstRegDate).exists()).toBe(true);
    expect(wrapper.findComponent(Holds).exists()).toBe(true);
    expect(wrapper.findComponent(Myplan).exists()).toBe(true);
    expect(wrapper.findComponent(MyplanCourses).exists()).toBe(true);
    expect(wrapper.findComponent(Resources).exists()).toBe(true);
  });
});
