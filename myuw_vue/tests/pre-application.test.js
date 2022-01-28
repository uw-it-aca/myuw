import axios from 'axios';

import { shallowMount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import profile from '../vuex/store/profile';

import GraduationPreApplication from '../components/home/graduation/pre-application.vue';
import javg001Profile from './mock_data/profile/javg001.json';
import javerageProfile from './mock_data/profile/javerage.json';
import jbothllProfile from './mock_data/profile/jbothell.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Graduation PreApplication Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        user: {
          affiliations: { 
            class_level: 'SENIOR',
            intl_stud: true,
            seattle: true,
            bothell: true,
            tacoma: true,
          }
        },
        termData: {
          quarter: 'spring',
          year: 2013,
        }
      },
    });
  });

  it('Verify show card', async () => {
    axios.get.mockResolvedValue({data: javg001Profile, status: 200});
    const wrapper = shallowMount(GraduationPreApplication, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.intlStudent).toBeTruthy();
    expect(wrapper.vm.curSenior).toBeTruthy();
    expect(wrapper.vm.seattle).toBeTruthy();
    expect(wrapper.vm.bothell).toBeTruthy();
    expect(wrapper.vm.tacoma).toBeTruthy();
    expect(wrapper.vm.classLevel).toBe('SENIOR');
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.term).toBe('2013,spring');
    expect(wrapper.findComponent(GraduationPreApplication).exists()).toBe(true);
  });
  it('Verify hide card if degree status is not 404', async () => {
    axios.get.mockResolvedValue({ data: javerageProfile, status: 200 });
    const wrapper = shallowMount(GraduationPreApplication, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.showCard).toBe(false);
  });
  it('Verify hide card if not a senior', async () => {
    store.state.user.affiliations.class_level = 'JUNIOR';
    axios.get.mockResolvedValue({ data: jbothllProfile, status: 200 });
    const wrapper = shallowMount(GraduationPreApplication, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.curSenior).toBe(false);
    expect(wrapper.vm.isReady).toBe(false);
  });
  it('Verify data error', async () => {
    axios.get.mockResolvedValue(Promise.reject({ response: { status: 404 } }));
    const wrapper = shallowMount(GraduationPreApplication, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.curSenior).toBe(true);
    expect(wrapper.vm.isErrored).toBe(true);
  });
});
 