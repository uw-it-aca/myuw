import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';

import HRPayrollCard from '../components/_common/hr-payroll.vue';
import UwCard from '../components/_templates/card.vue';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

describe('HR Payroll Card - Home Page', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        isHomePage: true,
        truncateView: false,
        user: {
          affiliations: {
            employee: false,
            student: false,
            stud_employee: false,
            instructor: false,
            retiree: false,
            past_employee: false,
            faculty: false,
          }
        }
      }
    });
  });

  const testCardHidden = (wrapper) => new Promise((done) => {
    try {
      expect(wrapper.vm.showCard).toBe(false);
    } catch (e) {
      done(e);
    }
    done();
  });

  const testCardVisible = (wrapper, store) => new Promise((done) => {
    try {
      expect(
        wrapper.findComponent(UwCard).exists()
      ).toBe(true);

      let h3s = wrapper.findAll('h3');
      let h4s = wrapper.findAll('h4');

      expect(
        h3s.at(0).text()
      ).toBe('HR and Payroll');

      expect(
        h4s.at(0).text()
      ).toBe('Workday');
      expect(
        h4s.at(0).classes()
      ).toContain('sr-only');

      let links = wrapper.findAll('a');

      let link1 = links.at(0);
      expect(link1.text()).toBe('Sign in to Workday');
      expect(link1.attributes().href
      ).toBe('https://wd5.myworkday.com/uw/login.htmld');

      if (!store.state.user.affiliations.stud_employee) {
        expect(
          h4s.at(1).text()
        ).toBe('Get Help');
  
        if (store.state.user.affiliations.faculty) {
          let link2 = links.at(1);
          expect(link2.text()).toBe('Academic HR');
          expect(link2.attributes().href
          ).toBe('https://ap.washington.edu/ahr/');
        } else {
          let link2 = links.at(1);
          expect(link2.text()).toBe('UW Human Resources');
          expect(link2.attributes().href
          ).toBe('https://hr.uw.edu/');
        }

        let link3 = links.at(2);
        expect(link3.text()).toBe('Integrated Service Center (ISC)');
        expect(link3.attributes().href
        ).toBe('https://isc.uw.edu/');

        if (!store.state.truncateView) {
          let link4 = links.at(3);
          expect(link4.text()).toBe('look up sick and vacation time');
          expect(link4.attributes().href
          ).toBe('https://isc.uw.edu/your-time-absence/time-off/');

          let link5 = links.at(4);
          expect(link5.text()).toBe('report time worked');
          expect(link5.attributes().href
          ).toBe('https://isc.uw.edu/your-time-absence/time-reporting/');

          let link6 = links.at(5);
          expect(link6.text()).toBe('update personal information');
          expect(link6.attributes().href
          ).toBe('https://isc.uw.edu/user-guides/edit_personal_information/');
        }
      } else {
        let link2 = links.at(1);
        expect(link2.text()).toBe('UW Human Resources');
        expect(link2.attributes().href
        ).toBe('https://hr.uw.edu/');
  
        let link3 = links.at(2);
        expect(link3.text()).toBe('Graduate Appointee Insurance Program (GAIP)');
        expect(link3.attributes().href
        ).toBe('https://hr.uw.edu/benefits/insurance/health/graduate-appointees/');

        let link4 = links.at(3);
        expect(link4.text()).toBe('Teaching or research assistant salary schedules');
        expect(link4.attributes().href
        ).toBe('https://grad.uw.edu/graduate-student-funding/funding-information-for-departments/administering-assistantships/ta-ra-salaries/');

        let link5 = links.at(4);
        expect(link5.text()).toBe('Integrated Service Center (ISC)');
        expect(link5.attributes().href
        ).toBe('https://isc.uw.edu/');

        let link6 = links.at(5);
        expect(link6.text()).toBe('enter your hours in Workday');
        expect(link6.attributes().href
        ).toBe('https://isc.uw.edu/your-time-absence/time-reporting/');

        let link7 = links.at(6);
        expect(link7.text()).toBe('set up direct deposit');
        expect(link7.attributes().href
        ).toBe('https://isc.uw.edu/your-pay-taxes/paycheck-info/#direct-deposit');
      }
    } catch (e) {
      done(e);
    }
    done();
  });

  it('Show HR-Payroll card for employee', () => {
    store.state.user.affiliations.employee = true;
    store.state.user.affiliations.faculty = true;
    return testCardVisible(mount(HRPayrollCard, { store, localVue }), store);
  });

  it('Show HR-Payroll card for retiree', () => {
    store.state.user.affiliations.retiree = true;
    store.state.truncateView = true;
    return testCardVisible(mount(HRPayrollCard, { store, localVue }), store);
  });

  it('Show HR-Payroll card for past-employee', () => {
    store.state.user.affiliations.past_employee = true;
    store.state.truncateView = true;
    return testCardVisible(mount(HRPayrollCard, { store, localVue }), store);
  });

  it('Show HR-Payroll card on Accounts page for instructor', () => {
    store.state.isHomePage = false;
    store.state.user.affiliations.instructor = true;
    return testCardVisible(mount(HRPayrollCard, { store, localVue }), store);
  });

  it('Show HR-Payroll card on Accounts page for stud_employee', () => {
    store.state.isHomePage = false;
    store.state.user.affiliations.stud_employee = true;
    return testCardVisible(mount(HRPayrollCard, { store, localVue }), store);
  });

  /* Hide card test cases */

  it('Hide HR-Payroll card from Account page', () => {
    store.state.isHomePage = false;
    return testCardHidden(mount(HRPayrollCard, { store, localVue }));
  });

  it('Hide HR-Payroll card for employee', () => {
    store.state.isHomePage = false;
    store.state.user.affiliations.employee = true;
    return testCardHidden(mount(HRPayrollCard, { store, localVue }));
  });

  it('Hide HR-Payroll card for student', () => {
    store.state.user.affiliations.student = true
    return testCardHidden(mount(HRPayrollCard, { store, localVue }));
  });

  it('Hide HR-Payroll card for instructor', () => {
    store.state.user.affiliations.instructor = true;
    return testCardHidden(mount(HRPayrollCard, { store, localVue }));
  });

});
