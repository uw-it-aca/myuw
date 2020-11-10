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
          }
        }
      }
    });
  });
  
  it('Display continuing education card', () => {

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

    let links = wrapper.findAll('a');
    expect(links.length).toEqual(5);

    let link1 = links.at(0);
    expect(link1.text()).toBe('About PCE');
    expect(link1.attributes().href
    ).toBe('https://www.pce.uw.edu');

    let link2 = links.at(1);
    expect(link2.text()).toBe('Career Accelerator Certificate Programs');
    expect(link2.attributes().href
    ).toBe('https://www.pce.uw.edu/career-accelerator-certificates');

    let link3 = links.at(2);
    expect(link3.text()).toBe('Certificate Programs');
    expect(link3.attributes().href
    ).toBe('https://www.pce.uw.edu/certificates');

    let link4 = links.at(3);
    expect(link4.text()).toBe('Degree Programs');
    expect(link4.attributes().href
    ).toBe('https://www.pce.uw.edu/degrees');

    let link5 = links.at(4);
    expect(link5.text()).toBe('Courses');
    expect(link5.attributes().href
    ).toBe('https://www.pce.uw.edu/courses');

  });
});

describe('User has 1st class affiliation', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            no_1st_class_affi: false,
          }
        }
      }
    });
  });

  it('Hide continuing education card', () => {
    const wrapper = shallowMount(ContinuingEducationCard,
                                 { store, localVue });
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });
});
