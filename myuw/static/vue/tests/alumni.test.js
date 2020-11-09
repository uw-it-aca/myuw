import { shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import AlumniCard from '../components/home/alumni.vue';
import UwCard from '../components/_templates/card.vue';
const localVue = createLocalVue(Vuex);

describe('User Is an Alumni', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            alumni: true,
          }
        }
      }
    });
  });

  it('Display Alumni Card', () => {
    const wrapper = shallowMount(AlumniCard, { store, localVue });
    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);
    expect(
      wrapper.findAll('h3').at(0).text()
    ).toBe('Alumni and Alumni Association');
    expect(
      wrapper.findAll('h4').at(0).text()
    ).toBe('University of Washington Alumni Association (UWAA)');
    expect(
      wrapper.findAll('a').at(0).text()
    ).toBe('Alumni News, Events and Services');
    expect(
      wrapper.findAll('a').at(0).attributes().hrep
    ).toBe('https://www.washington.edu/alumni');
    expect(
      wrapper.findAll('a').at(1).text()
    ).toBe('Columns Magazine');
    expect(
      wrapper.findAll('a').at(1).attributes().hrep
    ).toBe('https://magazine.washington.edu/');
    expect(
      wrapper.findAll('a').at(2).text()
    ).toBe('Learn about the UWAA');
    expect(
      wrapper.findAll('a').at(2).attributes().hrep
    ).toBe('https://www.washington.edu/cms/alumni/membership/');
  });

  describe('User Not an Alumni', () => {
    let store;
  
    beforeEach(() => {
      store = new Vuex.Store({
        state: {
          user: {
            affiliations: {
              alumni: false,
            }
          }
        }
      });
    });
  
    it('Hide Alumni Card', () => {
      const wrapper = shallowMount(AlumniCard, { store, localVue });
      expect(wrapper.findComponent(UwCard).exists()).toBe(false);
    });
  });
});
