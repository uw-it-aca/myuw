import axios from 'axios';
import {createLocalVue} from './helper';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import Textbooks from '../components/textbooks/textbooks.vue';
import Section from '../components/textbooks/section.vue';

import stud_schedule from '../vuex/store/schedule/student';
import inst_schedule from '../vuex/store/schedule/instructor';
import textbooks from '../vuex/store/textbooks';
import iac from '../vuex/store/iacourse-digital-material';

import javgBook from './mock_data//textbooks/javerage-iac-2013-spr.json';
import mockStudCourses from
  './mock_data/stud_schedule/javerage2013Spring.json';
import mockStudTextbook from './mock_data/textbooks/javerage-2013-spr.json';
import mockInstSche from './mock_data/inst_schedule/bill2013spr.json';
const mockTextbook = {
  "13830": {"error" : "-"},
  "13833": {"error": "-" },
  "18529": {"error": "-" },
  "18532": {"error": "-" },
  "18545": {"error": "-" },
  "order_url": null
};
import { library } from '@fortawesome/fontawesome-svg-core';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

const localVue = createLocalVue(Vuex);
jest.mock('axios');

describe('Textbook cards', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        inst_schedule,
        textbooks,
        iac,
      },
      state: {
        user: {
          affiliations: {
            seattle: true,
            student: true,
            bothell: true,
          }
        }
      }
    });
  });

  it('Verify with both student and teaching schedules', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/book/2013,spring': mockStudTextbook,
        '/api/v1/schedule/2013,spring': mockStudCourses,
        '/api/v1/instructor_schedule/2013,spring': mockInstSche,
        '/api/v1/iacourse/2013,spring': javgBook,
      };
      return Promise.resolve({data: urlData[url]});
    });

    let wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,spring'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.term).toEqual('2013,spring');
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.vm.orderUrl.length).toBe(150);
    expect(wrapper.vm.hasBookListed).toBe(true);

    const bookData = wrapper.vm.bookData;
    expect(bookData.year).toBe(2013);
    expect(bookData.quarter).toBe('spring');
    expect(bookData.collapseSections).toBe(true);
    expect(bookData.hasEnrolledSections).toBe(true);
    expect(bookData.sections.length).toBe(11);
    expect(bookData.hasTeachingSections).toBe(true);

    const section5 = wrapper.vm.bookData.enrolledSections[4];
    wrapper = mount(Section, {
      store, localVue,
      propsData: { 'section': section5}
    });
    expect(wrapper.vm.hasBook).toBeTruthy();
    expect(wrapper.vm.hasBookError).toBeFalsy();
    expect(wrapper.vm.orderBookUrl).toBeTruthy();
  });

  it('Verify other campus courses', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/v1/instructor_schedule/2013,spring') {
        return Promise.reject({response: {status: 404}});
      }
      const urlData = {
        '/api/v1/book/2013,spring': mockTextbook,
        '/api/v1/schedule/2013,spring': mockStudCourses,
        '/api/v1/iacourse/2013,spring': javgBook,
      };
      return Promise.resolve({data: urlData[url]});
    });

    let wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,spring'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.orderUrl).toBe(
      "https://ubookstore.com/pages/adoption-search/");
    const bookData = wrapper.vm.bookData;
    expect(bookData.sections.length).toBe(5);
    const seaSection = bookData.sections[1];
    const BotSection = bookData.sections[3];
    expect(BotSection.bothellCampus).toBe(true);
    const TacSection = bookData.sections[4];
    expect(TacSection.tacomaCampus).toBe(true);
  });

  it('Verify 404 book data error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 404}});
    });
    let wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,spring'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.bookData).toEqual({});
    expect(wrapper.vm.iacErrored).toEqual(false);
    expect(wrapper.vm.iacDataExist).toEqual(undefined);
  });
});
