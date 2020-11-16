import { shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import WorkdayLink from './components/_common/workday-link.vue';
import HRPayrollCard from '../components/_common/hr-payroll.vue';
import UwCard from '../components/_templates/card.vue';
const localVue = createLocalVue(Vuex);

localVue.component('myuw-workday-link', WorkdayLink);

describe('HR Payroll Card - Home Page', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        pageTitle: "Home",
        user: {
          affiliations: {
            employee: false,
            student: false,
            instructor: false,
            retiree: false,
            past_employee: false
          }
        }
      }
    });
  });

  function testCardVisible(userSettings){
    it('Card is visible', () => {
      store.state.user.affiliations.employee = userSettings["employee"];
      store.state.user.affiliations.student = userSettings["student"];
      store.state.user.affiliations.instructor = userSettings["instructor"];
      store.state.user.affiliations.retiree = userSettings["retiree"];
      store.state.user.affiliations.past_employee = userSettings["past_employee"];
      console.log(store.state);
      const wrapper = shallowMount(HRPayrollCard, { store, localVue });
      expect(
        wrapper.findComponent(UwCard).exists()
      ).toBe(true);
      expect(
        wrapper.findAll('h3').at(0).text()
      ).toBe('HR and Payroll');
    });
  }

  testCardVisible({'employee': true, 'student': false, 'instructor': false,
                   'retiree': false, 'past_empolyee': false})
  //testCardVisible({'employee': false, 'student': false, 'instructor': false,
  //                 'retiree': true, 'past_empolyee': false})
  //testCardVisible({'employee': false, 'student': false, 'instructor': false,
  //                 'retiree': false, 'past_empolyee': true}) 

});
