import axios from 'axios';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import notices from '../store/notices';
import NoticeCard from '../components/index/cards/notices';

import mockNotices from './mock_data/notices.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

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
    axios.get.mockResolvedValue({data: mockNotices});
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
    axios.get.mockResolvedValue({data: mockNotices});
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
    axios.get.mockResolvedValue({data: 'sdfsfsdg'});
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
    axios.get.mockResolvedValue({data: mockNotices});
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
    axios.get.mockResolvedValue({data: mockNotices});
    const wrapper = mount(NoticeCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();

    expect(wrapper.findAll('.p-0.notice-link')).toHaveLength(8);
    expect(wrapper.findAll('.collapse.show')).toHaveLength(0);

    for (let i = 0; i < 8; i++) {
      wrapper.findAll('.p-0.notice-link').at(i).trigger('click');
      await wrapper.vm.$nextTick();
    }
    expect(wrapper.findAll('.collapse.show')).toHaveLength(8);
  });

  it('Check show event', async () => {
    axios.get.mockResolvedValue({data: mockNotices});
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
