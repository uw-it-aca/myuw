import {shallowMount} from '@vue/test-utils';
import {createLocalVue} from './helper';
import Vuex from 'vuex';
import UwCard from '../components/_templates/card.vue';
import ContinuingEducationCard from '../components/home/former_student/ctnu-edu.vue';

const localVue = createLocalVue(Vuex);

describe('User has no 1st class affiliation', () => {

  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            no_1st_class_affi: true,
            student: false,
            past_student: false,
            employee: false,
            past_employee: false,
            applicant: false,
            instructor: false
          }
        }
      }
    });
  });
  
  it('Diplay continuing education card', () => {

    const wrapper = shallowMount(ContinuingEducationCard,
                                 {store, localVue});

    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);

    expect(
      wrapper.findAll('h3').at(0).text()
    ).toBe('Professional and Continuing Education (PCE)');

    expect(
      wrapper.findAll('h4').at(0).text()
    ).toBe('Available programs');

  });
});
