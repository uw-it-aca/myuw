import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import tuition from '../vuex/store/tuition';
import notices from '../vuex/store/notices';
import TuitionFees from '../components/accounts/tuition-fees.vue';
import jbotTuition from './mock_data/tuition/jbothell.json';
import jbotNotices from './mock_data/notice/jbothell.json';
import javgTuition from './mock_data/tuition/javerage.json';
import javgNotices from './mock_data/notice/javerage.json';

const localVue = createLocalVue(Vuex);
jest.mock('axios');

describe('Tuition store', () => {
  let store;
  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        tuition,
        notices,
      },
      state: {
        cardDisplayDates: {
          comparison_date: "2013-04-15T07:00:01",
        },
        user: {
          affiliations: {
            student: true,
            pce: false,
            grad_c2: false,
            undergrad_c2: false,
          }
        }
      }
    });
  });

  it('Evaluate the computed properties of jbothell', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': jbotNotices,
        '/api/v1/finance/': jbotTuition,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(TuitionFees, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.vm.isStudent).toBe(true);
    expect(wrapper.vm.isC2Grad).toBe(false);
    expect(wrapper.vm.isC2).toBe(false);
    expect(wrapper.vm.isPCE).toBe(false);
    expect(wrapper.vm.tuition.now).toBe(
      dayjs('2013-04-15T07:00:01'));
    expect(wrapper.vm.finAidNotices.length).toBe(1);
    expect(wrapper.vm.pceTuitionDup.length).toBe(0);
    expect(wrapper.vm.tuitionDate.date).toBe(dayjs("2014-08-20"));
    expect(wrapper.vm.tuitionDate.formatted ).toBe('');
    expect(wrapper.vm.tuitionDate.tuitionDue).toBe('');
    expect(wrapper.vm.tuitionDate.diff).toBe('');
  });
  it('Evaluate the computed properties of javerage', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': javgNotices,
        '/api/v1/finance/': javgTuition,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(TuitionFees, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
  });
});
