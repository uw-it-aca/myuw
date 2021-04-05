import axios from 'axios';
import {createLocalVue} from './helper';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import UwCard from '../components/_templates/card.vue';
import Textbooks from '../components/_common/textbooks.vue';
import stud_schedule from '../vuex/store/schedule/student';
import textbooks from '../vuex/store/textbooks';

import mockStudCourses from
  './mock_data/stud_schedule/javerage2013Spring.json';
import mockStudTextbook from './mock_data/textbooks/javerage-2013-spr.json';
const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Textbook card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        textbooks,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        },
        cardDisplayDates: {
          is_before_eof_7days_of_term: true,
        }
      }
    });
  });

  it('Show card', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/schedule/current': mockStudCourses,
        '/api/v1/book/current': mockStudTextbook,
      };
      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': 'current'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.term).toEqual('current');
    expect(wrapper.vm.isBeforeEndOfFirstWeek).toBe(true);
    expect(wrapper.vm.student ).toBe(true);
    expect(wrapper.vm.show).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    const bookData = wrapper.vm.bookData;
    expect(bookData.year).toBe(2013);
    expect(bookData.quarter).toBe('spring');
    expect(bookData.noBookAssigned).toBe(false);
    expect(bookData.sections.length).toBe(5);
  });

  it('Show card for future quarter', async () => {
    store.state.cardDisplayDates.is_before_eof_7days_of_term = false;
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/schedule/2013,summer': mockStudCourses,
        '/api/v1/book/2013,summer': mockStudTextbook,
      };
      return Promise.resolve({data: urlData[url]});
    });
    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,summer'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.show).toEqual(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });

  it('Hide card after display window', () => {
    store.state.cardDisplayDates.is_before_eof_7days_of_term = false;
    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': 'current'}});
    expect(wrapper.vm.show).toEqual(false);
  });

  it('Hide card if not student', () => {
    store.state.user.affiliations.student = false;
    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': 'current'}});
    expect(wrapper.vm.show).toEqual(false);
  });

  it('Show error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({status: 543});
    });
    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': 'current'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.show).toBe(true);
    expect(wrapper.vm.showError).toBe(true);
  });

  it('Hide error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({'status': 404});
    });
    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': 'current'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.show).toBe(true);
    expect(wrapper.vm.showError).toBe(false);
  });
});
