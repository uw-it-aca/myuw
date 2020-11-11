import { shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import RetireeCard from '../components/home/former_employee/retiree.vue';
import UwCard from '../components/_templates/card.vue';
const localVue = createLocalVue(Vuex);


describe('User is retireee', () => {

  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            retiree: true,
          }
        }
      }
    });
  });

  it('Display card if user is retiree', () => {
    const wrapper = shallowMount(RetireeCard,
                                 {store, localVue});

    expect(
      wrapper.findComponent(UwCard).exists()
    ).toBe(true);

    expect(
      wrapper.findAll('h3').at(0).text()
    ).toBe('UW Retirement Association (UWRA)');

    let links = wrapper.findAll('a');
    expect(links.length).toEqual(1);

    let link1 = links.at(0);
    expect(link1.text()).toBe('Learn more about UWRA');
    expect(link1.attributes().href
    ).toBe('http://www.washington.edu/uwra/');
  });

});
