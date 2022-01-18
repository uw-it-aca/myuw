import { shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import TranscriptsCard from '../components/home/former_student/transcripts.vue';
import UwCard from '../components/_templates/card.vue';
const localVue = createLocalVue(Vuex);

describe('Order Transcripts Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            past_stud: false,
          }
        }
      }
    });
  });

  it('Hide card if not pastStudent', () => {
    const wrapper = shallowMount(TranscriptsCard, {store, localVue});
    expect(wrapper.vm.pastStudent).toBeFalsy();
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Show card for past students', () => {
    store.state.user.affiliations.past_stud = true;
    const wrapper = shallowMount(TranscriptsCard, {store, localVue});
    expect(wrapper.vm.pastStudent).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });
});
