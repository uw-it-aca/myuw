import axios from 'axios';

import { shallowMount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import profile from '../vuex/store/profile';

import StudentProfileCard from '../components/profile/student-profile.vue';
import javg001Profile from './mock_data/profile/javg001.json';
import javg002Profile from './mock_data/profile/javg002.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Student Profile Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        user: {
          affiliations: { 
            employee: true,
            stud_employee: true,
          }
        }
      },
    });
  });

  it('Verify computed properties', async () => {
    axios.get.mockResolvedValue({data: javg002Profile, status: 200});
    const wrapper = shallowMount(StudentProfileCard, {store, localVue});
    await new Promise(setImmediate);

    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.existClassLevel).toBeTruthy();
    expect(wrapper.vm.existResidency).toBeTruthy();
    expect(wrapper.vm.showResidency).toBeTruthy();
    expect(wrapper.vm.formatResidency(
      wrapper.vm.residentCode, wrapper.vm.residentDesc).toBe("NONRESIDENT"));
    expect(wrapper.vm.hasPendingResidency).toBeTruthy();
    expect(wrapper.vm.pendingResidency.term.quarter).toBe("autumn");
    expect(wrapper.vm.termMajors).toBeTruthy();
    expect(wrapper.vm.hasMinors).toBeTruthy();
    expect(wrapper.vm.termMinors).toBeTruthy();
    expect(wrapper.vm.localAddress).toBeTruthy();
    expect(wrapper.vm.permanentAddress).toBeTruthy();
  });

  it('addressLocationString()', async () => {
    axios.get.mockResolvedValue({data: javg001Profile, status: 200});
    const wrapper = shallowMount(StudentProfileCard, {store, localVue});
    await new Promise(setImmediate);

    expect(
      wrapper.vm.addressLocationString(wrapper.vm.permanentAddress)
    ).toEqual('Bellevue, WA 98005-1234');

    expect(
      wrapper.vm.addressLocationString({
        city: 'Seattle',
        state: 'WA',
      })
    ).toEqual('Seattle, WA');

    expect(
      wrapper.vm.addressLocationString({
        city: null,
        state: null,
        country: null,
      })
    ).toEqual('');
  });
});
 