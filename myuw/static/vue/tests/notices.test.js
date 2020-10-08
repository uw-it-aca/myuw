import axios from 'axios';
import {mount, shallowMount} from '@vue/test-utils';
import { BCollapse } from 'bootstrap-vue'
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import notices from '../vuex/store/notices';
import NoticeCard from '../components/pages/home/cards/notices';
import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();
localVue.component('font-awesome-icon', FontAwesomeIcon);

jest.mock('axios');

describe('Notice Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        notices,
      },
    });
  });

  it('Check status changes on fetch', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    expect(
        notices.getters.isFetching(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
        notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeFalsy();
  });

  it('Check second fetch', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    expect(
        notices.getters.isFetching(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
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
    await new Promise((r) => setTimeout(r, 10));
    expect(
        notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeFalsy();
  });

  it('Check postProcess fields', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = shallowMount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
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
        expect(notice.date).toBeInstanceOf(Date);
      }
    });
  });

  it('Check notices populate and click', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = mount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.findAll('button')).toHaveLength(8);
    expect(wrapper.findAllComponents(BCollapse)).toHaveLength(8);

    for (let i = 0; i < 8; i++) {
      expect(wrapper.findAllComponents(BCollapse).at(i).vm.show).toBeFalsy();
      await wrapper.findAll('button').at(i).trigger('click');
      expect(wrapper.findAllComponents(BCollapse).at(i).vm.show).toBeTruthy();
    }
  });

  it('Check show event', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    axios.put = jest.fn(() => Promise.resolve());
    const wrapper = mount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();

    wrapper.vm.notices.forEach((notice) => {
      wrapper.vm.onShowNotice(notice);
    });
    expect(axios.put).toHaveBeenCalledTimes(8);

    // Test that it is not called twice
    wrapper.vm.notices.forEach((notice) => {
      notice.is_read = true;
      wrapper.vm.onShowNotice(notice);
    });
    expect(axios.put).toHaveBeenCalledTimes(8);
  });
});
