import axios from 'axios';
import {createLocalVue} from './helper';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';

import UwPanel from '../components/_templates/panel.vue';
import Textbooks from '../components/textbooks/textbooks.vue';
import Section from '../components/textbooks/section.vue';
import Covid from '../components/textbooks/covid.vue';
import Book from '../components/textbooks/book.vue';
import LinkButton from '../components/_templates/link-button.vue';

import stud_schedule from '../vuex/store/schedule/student';
import inst_schedule from '../vuex/store/schedule/instructor';
import textbooks from '../vuex/store/textbooks';

import mockStudCourses from
  './mock_data/stud_schedule/javerage2013Spring.json';
import mockStudTextbook from './mock_data/textbooks/javerage-2013-spr.json';
import mockInstSche from './mock_data/inst_schedule/bill2013spr.json';
const mockTextbook = {
  "13830": [],
  "13833": [],
  "18529": [],
  "18532": [],
  "18545": [],
  "order_url": null
};
import { library } from '@fortawesome/fontawesome-svg-core';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

const localVue = createLocalVue(Vuex);
localVue.component('uw-panel', UwPanel);
jest.mock('axios');

describe('Textbook cards', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        inst_schedule,
        textbooks,
      },
    });
  });

  it('Verify with both student and teaching sches', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/book/2013,spring': mockStudTextbook,
        '/api/v1/schedule/2013,spring': mockStudCourses,
        '/api/v1/instructor_schedule/2013,spring': mockInstSche,
      };
      return Promise.resolve({data: urlData[url]});
    });

    const wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,spring'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.term).toEqual('2013,spring');
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.isErrored).toBe(false);
    expect(wrapper.findComponent(UwPanel).exists()).toBe(true);
    expect(wrapper.findAllComponents(Section).length).toBe(11);
    expect(wrapper.findAllComponents(Book).length).toBe(6);
    expect(wrapper.findComponent(LinkButton).exists()).toBe(true);
    expect(wrapper.findComponent(Covid).exists()).toBe(true);
    expect(wrapper.vm.orderUrl).toBe(
      "http://www.ubookstore.com/adoption-search-results?ccid=9335,1132,5320,2230,4405");
    const bookData = wrapper.vm.bookData;
    expect(bookData.year).toBe(2013);
    expect(bookData.quarter).toBe('spring');
    expect(bookData.collapseSections).toBe(true);
    expect(bookData.enrolledSections.length).toBe(5);
    expect(bookData.sections.length).toBe(11);
    expect(bookData.hasTeachingSections).toBe(true);
  });

  it('Verify other campus courses', async () => {
    axios.get.mockImplementation((url) => {
      if (url === '/api/v1/instructor_schedule/2013,spring') {
        return Promise.reject({response: {status: 404}});
      }
      const urlData = {
        '/api/v1/book/2013,spring': mockTextbook,
        '/api/v1/schedule/2013,spring': mockStudCourses,
      };
      return Promise.resolve({data: urlData[url]});
    });

    let wrapper = mount(Textbooks, {store, localVue,
      propsData: {'term': '2013,spring'}});
    await new Promise(setImmediate);
    expect(wrapper.vm.orderUrl).toBe(
      "http://www.ubookstore.com/adoption-search");
    const bookData = wrapper.vm.bookData;
    expect(bookData.sections.length).toBe(5);
    const seaSection = bookData.sections[1];
    const BotSection = bookData.sections[3];
    expect(BotSection.bothellCampus).toBe(true);
    const TacSection = bookData.sections[4];
    expect(TacSection.tacomaCampus).toBe(true);

    wrapper = mount(Section, {store, localVue,
      propsData: {'section': seaSection}});
    await new Promise(setImmediate);
    expect(wrapper.vm.teachingOrderBookUrl).toBe(
      "http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwmain"
    );

    wrapper = mount(Section, {store, localVue,
      propsData: {'section': BotSection}});
    await new Promise(setImmediate);
    expect(wrapper.vm.teachingOrderBookUrl).toBe(
      "http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwbothell"
    );

    wrapper = mount(Section, {store, localVue,
      propsData: {'section': TacSection}});
    await new Promise(setImmediate);
    expect(wrapper.vm.teachingOrderBookUrl).toBe(
      "http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=uwtacoma"
    );
  });
});
