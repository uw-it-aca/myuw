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

  it('Verify content', async () => {
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
    expect(wrapper.vm.orderUrl).toBe("http://www.ubookstore.com/adoption-search");
    const bookData = wrapper.vm.bookData;
    expect(bookData.year).toBe(2013);
    expect(bookData.quarter).toBe('spring');
    expect(bookData.collapseSections).toBe(true);
    expect(bookData.enrolledSections.length).toBe(5);
    expect(bookData.sections.length).toBe(11);
    expect(bookData.hasTeachingSections).toBe(true);
    
  });
});
