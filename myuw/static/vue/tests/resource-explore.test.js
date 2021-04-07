import { shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import ResourcesExplore from '../components/home/resources/resource-explore.vue';
import UwCard from '../components/_templates/card.vue';
const localVue = createLocalVue(Vuex);

describe('Resources Explore Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
    });
  });

  it('Show ResourcesExplore card', () => {
    const wrapper = shallowMount(ResourcesExplore, {store, localVue});
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });
});
