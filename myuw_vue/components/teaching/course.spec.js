import { mount } from '@cypress/vue';
import Vuex from 'vuex';

import classlist from '../../vuex/store/classlist';
import emaillist from '../../vuex/store/emaillist';
import inst_schedule from '../../vuex/store/schedule/instructor';

import courseMixin from '../../mixins/courses';

import CourseCards from './course/course_cards.vue';

describe('<CourseCards />', () => {
  it('Course Cards', () => {
    const TERM = '2013,spring';

    cy.intercept(
      'GET',
      `/api/v1/instructor_schedule/${TERM}`,
      {fixture: 'inst_schedule/bill2013spr.json'}
    );
    // cy.intercept('GET', '/api/v1/instructor_section_details/*/*', {});

    cy.createLocalVue(Vuex).then((localVue) => {
      localVue.mixin(courseMixin);
      let store = new Vuex.Store({
        modules: {
          classlist,
          emaillist,
          inst_schedule,
        }
      });

      mount(CourseCards, {store, localVue, propsData: {term: TERM}}).then(() => {
        cy.componentWaitUntil((vm) => vm.isReady || vm.isErrored);
        // TODO: take image snapshot here
      });
    });
  });
});