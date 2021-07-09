import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import tuition from '../vuex/store/tuition';
import notices from '../vuex/store/notices';
import TuitionFees from '../components/accounts/tuition-fees.vue';
import TuitionRes from '../components/accounts/tuition-resources.vue';
import CardStatus from '../components/_templates/card-status.vue';
import LinkButton from '../components/_templates/link-button.vue';
import FinAid from '../components/_common/finaid.vue';

import jbotTuition from './mock_data/tuition/jbothell.json';
import jbotNotices from './mock_data/notice/jbothell.json';
import javgTuition from './mock_data/tuition/javerage.json';
import javgNotices from './mock_data/notice/javerage.json';
import gc2Tuition from './mock_data/tuition/grad-c2.json';
import gc2Notices from './mock_data/notice/grad-c2.json';

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
          comparison_date: "2013-04-15T00:00:01",
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
    await new Promise(setImmediate);

    expect(wrapper.vm.isStudent).toBe(true);
    expect(wrapper.vm.isC2Grad).toBe(false);
    expect(wrapper.vm.isC2).toBe(false);
    expect(wrapper.vm.isPCE).toBe(false);
    expect(wrapper.vm.notices.length).toBe(14);
    expect(wrapper.vm.finAidNotices.length).toBe(1);
    expect(wrapper.vm.pceTuitionDup.length).toBe(0);
    expect(wrapper.vm.tuitionDate.formatted ).toBe('Wed, Aug 20');
    expect(wrapper.vm.pceBalance).toBe(0);
    expect(wrapper.vm.tuiBalance).toBe(1);
    expect(wrapper.findComponent(TuitionFees).exists()).toBe(true);
    expect(wrapper.findComponent(LinkButton).exists()).toBe(true);
    expect(wrapper.findComponent(FinAid).exists()).toBe(true);
    expect(wrapper.findComponent(TuitionRes).exists()).toBe(true);
    expect(wrapper.findAllComponents(CardStatus).length).toBe(2);
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
    await new Promise(setImmediate);
    expect(wrapper.vm.tuitionDate.formatted ).toBe("Mon, Feb 22");
    expect(wrapper.vm.pceBalance).toBe(1000.00);
    expect(wrapper.vm.tuiBalance).toBe(12345.00);
    expect(Boolean(wrapper.vm.tuitionDate)).toBe(true);
    expect(wrapper.vm.finAidNotices.length).toBe(5);
    expect(wrapper.vm.tuitionDueNotice.attributes.length).toBe(1);
    expect(wrapper.findComponent(TuitionFees).exists()).toBe(true);
    expect(wrapper.findComponent(LinkButton).exists()).toBe(true);
    expect(wrapper.findComponent(FinAid).exists()).toBe(true);
    expect(wrapper.findComponent(TuitionRes).exists()).toBe(true);
    expect(wrapper.findAllComponents(CardStatus).length).toBe(3);
  });

  it('Evaluate the computed properties of jpce', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/notices/': gc2Notices,
        '/api/v1/finance/': gc2Tuition,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(TuitionFees, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.findAllComponents(CardStatus).length).toBe(3);
    expect(wrapper.vm.tuitionDate.formatted ).toBe("Fri, Jul 9");
    expect(wrapper.vm.pceBalance).toBe(2897.00);
    expect(wrapper.vm.tuiBalance).toBe(-10.00);
  });
});
