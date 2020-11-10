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
    
    let link1 = wrapper.findAll('a').at(0);
    expect(link1.text()).toBe('Alumni News, Events and Services');
    expect(link1.attributes().href
    ).toBe('https://www.washington.edu/alumni');

    let link2 = wrapper.findAll('a').at(1);
    expect(link2.text()).toBe('Columns Magazine');
    expect(link2.attributes().href
    ).toBe('https://magazine.washington.edu/');

    let link3 = wrapper.findAll('a').at(2)
    expect(link3.text()).toBe('Learn about the UWAA');
    expect(link3.attributes().href
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
