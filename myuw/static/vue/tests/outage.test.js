import {shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import Outage from '../components/_common/outage.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';

import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

const localVue = createLocalVue(Vuex);

library.add(faExclamationTriangle);
localVue.component('font-awesome-icon', FontAwesomeIcon);

const propData = {
  term: 'current',
};

describe('Outage card', () => {

  it('non404Error checking', () => {
    let store = new Vuex.Store({
        state: {
          user: {
            affiliations: {
            student: true,
            instructor: false,
            employee: false,
            }
          }
        },
        getters: {
          'stud_schedule/statusCodeTagged': () => function () { return 200; },
          'notices/statusCode': () => 200,
          'profile/statusCode': () => 200,
        },
    });
    const wrapper = shallowMount(Outage, {store, localVue, propData});
    expect(wrapper.vm.non404Error(200)).toBeFalsy();
    expect(wrapper.vm.non404Error(404)).toBeFalsy();
    expect(wrapper.vm.non404Error(543)).toBeTruthy();
    expect(wrapper.vm.non404Error(400)).toBeTruthy();
  });

  describe('showOutageCard for Student', () => {
    const state = {
      user: {
        affiliations: {
          student: true,
          instructor: false,
          employee: false,
        }
      }
    };

    it('showOutageCard for Student - Successful calls', () => {
      let getters = {
        'stud_schedule/statusCodeTagged': () => function () { return 200; },
        'notices/statusCode': () => 200,
        'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });

      const wrapper = shallowMount(Outage, {store, localVue, propData});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 404 Error', () => {
      let getters = {
        'stud_schedule/statusCodeTagged': () => function () { return 404; },
        'notices/statusCode': () => 200,
        'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });
  
      const wrapper = shallowMount(Outage, {store, localVue, propData});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 543 Error', () => {
      let getters = {
        'stud_schedule/statusCodeTagged': () => function () { return 543; },
        'notices/statusCode': () => 200,
        'profile/statusCode': () => 200,
      };
      let store = new Vuex.Store({
        getters,
        state,
      });
    
      const wrapper = shallowMount(Outage, {store, localVue, propData});
      expect(wrapper.vm.showOutageCard).toBeTruthy();
    });
  });
  // TODO: Add tests for the instructor and employee status'
  // This currently only tests for the case of a student.

});