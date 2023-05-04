import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import notices from '../vuex/store/notices';
import profile from '../vuex/store/profile';

import DeclareMajorCard from '../components/home/major-declaration/declare-major.vue';
import CurMajors from '../components/_common/cur_major.vue';
import mockNotices from './mock_data/notice/jinter.json';
import javg005Profile from './mock_data/profile/javg005.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Student Profile Card', () => {
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
          }
        }
      },
    });
  });

  it('Verify computed properties', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': mockNotices,
        '/api/v1/profile/': javg005Profile,
      };
      return Promise.resolve({ data: urlData[url] });
    });
    const wrapper = mount(DeclareMajorCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isJunior).toBe(true);
    expect(wrapper.vm.showContent).toBe(true);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.vm.hasRegHolds).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.findAllComponents(DeclareMajorCard)).toHaveLength(1);
    expect(wrapper.findAllComponents(CurMajors)).toHaveLength(1);
    expect(wrapper.findAll('h3').length).toBe(6);
  });
});
