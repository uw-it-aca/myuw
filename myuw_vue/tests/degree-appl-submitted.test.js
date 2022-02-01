import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import profile from '../vuex/store/profile';

import Graduation from '../components/home/graduation/application-submitted.vue';
import eightProfile from './mock_data/profile/eight.json';
import javg001Profile from './mock_data/profile/javg001.json';
import javg002Profile from './mock_data/profile/javg002.json';
import javg003Profile from './mock_data/profile/javg003.json';
import javg004Profile from './mock_data/profile/javg004.json';
import javerageProfile from './mock_data/profile/javerage.json';
import jbothllProfile from './mock_data/profile/jbothell.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Graduation Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        user: {
          affiliations: {
            latest_class_level: 'SENIOR',
            intl_stud: true,
          }
        },
        termData: {
          quarter: 'spring',
          year: 2013,
        }
      },
    });
  });

  it('Verify single degree', async () => {
    axios.get.mockResolvedValue({ data: javerageProfile, status: 200});
    const wrapper = mount(Graduation, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.intlStudent).toBeTruthy();
    expect(wrapper.vm.graduatingSenior).toBeTruthy();
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.showContent).toBe(true);
    // expect(wrapper.vm.showError).toBe(false);
    expect(wrapper.vm.hasDoubleDegrees).toBe(false);
    expect(wrapper.vm.doubleDegreeDiffStatus).toBe(false);
    expect(wrapper.vm.doubleDegreesInDiffTerms).toBe(false);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringAprilMay).toBe(true);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringEarnedTerm).toBe(false);
    expect(wrapper.vm.hasActiveApplBeforeEarnedTerm).toBe(true);
    expect(wrapper.vm.hasActiveApplication).toBe(true);
    expect(wrapper.vm.hasGrantedDegree).toBe(false);
    expect(wrapper.vm.seattle).toBeTruthy();
    expect(wrapper.vm.bothell).toBe(false);
    expect(wrapper.vm.tacoma).toBe(false);
    expect(wrapper.vm.diplomaName).toBe("John Joseph Average");
    expect(wrapper.findComponent(Graduation).exists()).toBe(true);
  });
  it('Verify double degrees diff terms', async () => {
    axios.get.mockResolvedValue({ data: javg004Profile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.hasDoubleDegrees).toBe(true);
    expect(wrapper.vm.doubleDegreeDiffStatus).toBe(false);
    expect(wrapper.vm.doubleDegreesInDiffTerms).toBe(true);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringAprilMay).toBe(true);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringEarnedTerm).toBe(true);
    expect(wrapper.vm.hasActiveApplBeforeEarnedTerm).toBe(true);
    expect(wrapper.vm.hasActiveApplication).toBe(true);
    expect(wrapper.vm.hasGrantedDegree).toBe(false);
  });
  it('Verify double degrees diff status', async () => {
    axios.get.mockResolvedValue({ data: eightProfile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.hasDoubleDegrees).toBe(true);
    expect(wrapper.vm.doubleDegreeDiffStatus).toBe(true);
    expect(wrapper.vm.doubleDegreesInDiffTerms).toBe(false);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringAprilMay).toBe(true);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringEarnedTerm).toBe(true);
    expect(wrapper.vm.hasActiveApplBeforeEarnedTerm).toBe(false);
    expect(wrapper.vm.hasActiveApplication).toBe(false);
    expect(wrapper.vm.hasGrantedDegree).toBe(true);
    expect(wrapper.vm.seattle).toBe(false);
    expect(wrapper.vm.bothell).toBe(false);
    expect(wrapper.vm.tacoma).toBe(true);
  });
  it('Verify double degrees same status same term', async () => {
    axios.get.mockResolvedValue({ data: javg003Profile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.hasDoubleDegrees).toBe(true);
    expect(wrapper.vm.doubleDegreeDiffStatus).toBe(false);
    expect(wrapper.vm.hasActiveApplBeforeEarnedTerm).toBe(false);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringAprilMay).toBe(true);
    expect(wrapper.vm.hasActiveOrGrantedDegreeDuringEarnedTerm).toBe(true);
    expect(wrapper.vm.hasActiveApplication).toBe(true);
    expect(wrapper.vm.hasGrantedDegree).toBe(false);
  });
  it('Verify hide card if degree status is 404', async () => {
    axios.get.mockResolvedValue({ data: javg001Profile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate)
    expect(wrapper.vm.showCard).toBe(false);
    expect(wrapper.vm.showError).toBe(false);
  });
  it('Verify hide card if not graduation senior', async () => {
    store.state.user.affiliations.latest_class_level = 'JUNIOR';
    axios.get.mockResolvedValue({ data: jbothllProfile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.graduatingSenior).toBe(false);
    expect(wrapper.vm.showCard).toBe(false);
  });
  it('Verify show error', async () => {
    // degree_status.error_code: 503
    axios.get.mockResolvedValue({ data: javg002Profile, status: 200 });
    const wrapper = mount(Graduation, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.graduatingSenior).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
  });
});
