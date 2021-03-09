import axios from 'axios';
import dayjs from 'dayjs';
import {shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import hfs from '../vuex/store/hfs';
import library from '../vuex/store/library';
import Summaries from '../components/home/summaries.vue';

import mockNotices from './mock_data/notice/javerage.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');
jest.mock('dayjs');

describe('Summaries', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        hfs,
        library,
      },
      state: {},
    });
  });

  it('toFromNowDate', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    dayjs.mockImplementation((s) => {
      return {
        fromNow: jest.fn().mockReturnValueOnce(s),
      };
    });
    const wrapper = shallowMount(Summaries, {store, localVue});
    expect(wrapper.vm.toFromNowDate('test')).toEqual('test');
    expect(dayjs).toHaveBeenCalledTimes(1);
  });

  it('getWeeksApart', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = shallowMount(Summaries, {store, localVue});
    dayjs.mockImplementation(jest.requireActual('dayjs'));

    // The week starts on Sundays
    // Winter quarter starts on Tuesday
    let d1 = new Date(2017, 0, 3);
    let d2 = null;
    for (let i = 25; i <= 31; i++) {
      d2 = new Date(2016, 11, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);
    }

    for (let i = 1; i <= 7; i++) {
      d2 = new Date(2017, 0, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);
    }

    for (let i = 8; i <= 14; i++) {
      d2 = new Date(2017, 0, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(2);
    }

    for (let i = 12; i <= 18; i++) {
      d2 = new Date(2017, 2, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(11);
    }

    d2 = new Date(2017, 2, 21);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(12);

    // Spring quarter starts on Monday
    d1 = new Date(2017, 2, 27);
    d2 = new Date(2017, 2, 22);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);

    d2 = new Date(2017, 2, 26);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);

    d1 = new Date(2017, 2, 27);
    d2 = new Date(2017, 3, 1);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);

    // Aut quarter starts on Wedesnday
    d1 = new Date(2017, 8, 27);
    d2 = new Date(2017, 8, 23);
    expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);

    for (let i = 24; i <= 30; i++) {
      d2 = new Date(2017, 8, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(1);
    }
    for (let i = 10; i <= 23; i++) {
      d2 = new Date(2017, 8, i);
      expect(wrapper.vm.getWeeksApart(d1, d2)).toEqual(0);
    }
  });
});
