import axios from 'axios';
import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import notices from '../vuex/store/notices';
import NoticeCard from '../components/home/notice/notices';

import javgNotices from './mock_data/notice/javerage.json';
import jnewNotices from './mock_data/notice/jnew.json';
import jbotNotices from './mock_data/notice/jbothell.json';

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

    wrapper.vm.notices.forEach((notice) => {
      wrapper.vm.onShowNotice(notice);
    });
    expect(axios.put).toHaveBeenCalledTimes(9);

    // Test that it is not called twice
    wrapper.vm.notices.forEach((notice) => {
      notice.is_read = true;
      wrapper.vm.onShowNotice(notice);
    });
    expect(axios.put).toHaveBeenCalledTimes(9);
  });
});
