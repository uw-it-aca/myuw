import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import profile from '../vuex/store/profile';

import DeclareMajorCard from '../components/home/major-declaration/declare-major.vue';
import MajorSea from '../components/home/major-declaration/major-sea.vue';
import MajorBot from '../components/home/major-declaration/major-bot.vue';
import MajorTac from '../components/home/major-declaration/major-tac.vue';
import CurMajors from '../components/_common/major/cur-fut-majors.vue';
import mockNotices from './mock_data/notice/jinter.json';
import premajorProfile from './mock_data/profile/javgPremajor.json';
import javg005Profile from './mock_data/profile/javg005.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Declare Major Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
        profile,
      },
      state: {
        user: {
          affiliations: { 
            class_level: 'JUNIOR',
            seattle: true,
          }
        }
      },
    });
  });

  it('Verify with a seattle junior of premajor', async () => {
    // MUWM-5144
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/profile/': premajorProfile
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(DeclareMajorCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isJunior).toBe(true);
    expect(wrapper.vm.seattle).toBe(true);
    expect(wrapper.vm.notDeclaredMajor).toBe(true);
    expect(wrapper.vm.showContent).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.hasRegHolds).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.findAllComponents(DeclareMajorCard)).toHaveLength(1);
    expect(wrapper.findAllComponents(CurMajors)).toHaveLength(1);
    expect(wrapper.findAllComponents(MajorSea)).toHaveLength(1);
    expect(wrapper.findAll('h3').length).toBe(6);
    expect(wrapper.vm.reviewOptionsUrl).toHaveLength(63);
  });

  it('Verify junior with declared major, hide card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/profile/': javg005Profile
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(DeclareMajorCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isJunior).toBe(true);
    expect(wrapper.vm.notDeclaredMajor).toBe(false);
    expect(wrapper.vm.showCard).toBe(false);
  });
  it('Verify Bothell case', async () => {
    // MUWM-5296
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.bothell = true;
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/profile/': premajorProfile
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(DeclareMajorCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.bothell).toBe(true);
    expect(wrapper.vm.isTargetViewer).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.reviewOptionsUrl).toHaveLength(56);
    expect(wrapper.findAllComponents(MajorBot)).toHaveLength(1);
  });
  it('Verify Tacoma case', async () => {
    // MUWM-5297
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.tacoma = true;
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/profile/': premajorProfile
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(DeclareMajorCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.tacoma).toBe(true);
    expect(wrapper.vm.isTargetViewer).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.reviewOptionsUrl).toHaveLength(69);
    expect(wrapper.findAllComponents(MajorTac)).toHaveLength(1);
  });
});
