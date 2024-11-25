import axios from 'axios';
import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import notices from '../vuex/store/notices';
import NoticeCard from '../components/home/notice/notices';
import NoticeList from '../components/home/notice/notice-items';
import CollapsedItem from '../components/_common/collapsed-notice.vue';

import javgNotices from './mock_data/notice/javerage.json';
import jnewNotices from './mock_data/notice/jnew.json';
import noNotices from './mock_data/notice/none.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Notice Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        }
      }
    });
  });

  it('Check status changes on fetch', async () => {
    axios.get.mockResolvedValue({data: javgNotices, status: 200});
    const wrapper = mount(NoticeCard, {store, localVue});
    expect(
        notices.getters.isFetching(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
        notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeFalsy();
    expect(wrapper.vm.notices.length).toBe(9);
    expect(wrapper.vm.notices[1].category).toBe("MyUW Banner Notice");
    expect(wrapper.vm.notices[1].startDate).toBeInstanceOf(dayjs);
  });

  it('Check second fetch', async () => {
    axios.get.mockResolvedValue({data: javgNotices, status: 200});
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    expect(
        notices.getters.isFetching(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    wrapper.vm.$store.dispatch('notices/fetch');
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
  });

  it('Check status when fetch fails', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(
        notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeFalsy();
  });

  it('Check postProcess fields', async () => {
    axios.get.mockResolvedValue({data: jnewNotices, status: 200});
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();

    const parser = new DOMParser();
    wrapper.vm.$store.state.notices.value.forEach((notice) => {
      if ('notice_title' in notice) {
        const htmlDoc = parser.parseFromString(
            notice.notice_title, 'text/html');
        expect(
            htmlDoc.getElementsByClassName('notice-title'),
        ).toHaveLength(1);
      }
      if ('notice_body' in notice) {
        const htmlDoc = parser.parseFromString(
            notice.notice_body, 'text/html');
        expect(
            htmlDoc.getElementsByClassName('notice-body-with-title'),
        ).toHaveLength(1);
      }
      if ('date' in notice) {
        // expect(notice.date).toBeInstanceOf(Date);  <==dayjs
      }
    });
  });

  it('Check show event', async () => {
    axios.get.mockResolvedValue({data: javgNotices, status: 200});
    axios.put = jest.fn(() => Promise.resolve());
    const wrapper = mount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();

    const wrapper1 = mount(NoticeList, {
      store, localVue, propsData: {
        notices: wrapper.vm.notices,
      }
    });
    
    wrapper1.vm.notices.forEach((notice) => {
      const wrapper2 = mount(CollapsedItem, {
        store, localVue, propsData: {
          notice: notice,
          callerId: "noticeCard"
        }
      });
      expect(wrapper2.vm.collapseOpen).toBe(false);
      wrapper2.vm.onShowNotice(notice);
    });

    expect(axios.put).toHaveBeenCalledTimes(9);

    // Test that it is not called twice
    wrapper1.vm.notices.forEach((notice) => {
      const wrapper2 = mount(CollapsedItem, {
        store, localVue, propsData: {
          notice: notice,
          callerId: "noticeCard"
        }
      });
      notice.is_read = true;
      wrapper2.vm.onShowNotice(notice);
    });
    expect(axios.put).toHaveBeenCalledTimes(9);
  });

  it('Check display components', async () => {
    axios.get.mockResolvedValue({ data: javgNotices, status: 200 });
    const wrapper = mount(NoticeCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.notices.length).toBe(9);
    expect(wrapper.findComponent(NoticeCard).exists()).toBe(true);
    expect(wrapper.findComponent(NoticeList).exists()).toBe(true);
    expect(wrapper.findComponent(CollapsedItem).exists()).toBe(true);
  });

  it('Check display do not have any notices', async () => {
    axios.get.mockResolvedValue({ data: noNotices, status: 200 });
    const wrapper = mount(NoticeCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.vm.noDisplayableNotices).toBe(true);
    expect(wrapper.findComponent(NoticeCard).exists()).toBe(true);
  });
});
