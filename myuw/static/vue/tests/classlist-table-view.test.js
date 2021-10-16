import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue, deepClone } from './helper';

import Vuex from 'vuex';
import classlist from '../vuex/store/classlist';

import mockBilljoint2013Aut from
  './mock_data/classlist/2013-autumn-POLS-306-A.json';
import mockBilljoint2013AutCOM306A from
  './mock_data/classlist/2013-autumn-COM-306-A.json';

import Classlist from '../components/teaching/classlist/class-student-list.vue';
import ClasslistContent from '../components/teaching/classlist/content.vue';
import TableView from '../components/teaching/classlist/table-view.vue';
import CourseStats from '../components/teaching/classlist/statistics.vue';
import UwTable from '../components/_templates/card-table.vue';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Show Classlist Content', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        classlist,
      },
      state: {
        user: {
          affiliations: {
            instructor: true,
          }
        },
      }
    });
  });

  it('POL S 306 A Autumn 2013 Content', async () => {
    axios.get.mockImplementation((url) => {
      if (url.endsWith("CSE,306/A")) {
        return Promise.reject({response: {status: 403}});
      }
      const urlData = {
        '/api/v1/instructor_section_details/2013,autumn,POL S,306/A': deepClone(
          mockBilljoint2013Aut),
        '/api/v1/instructor_section_details/2013,autumn,COM,306/A': deepClone(
          mockBilljoint2013AutCOM306A),
      };
      return Promise.resolve({data: urlData[url], status: 200});
    });

    let wrapper = mount(Classlist, 
      { store,
        localVue,
        propsData: {'sectionLabel': "2013,autumn,POL S,306/A"}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.showCard).toBeTruthy();
    expect(wrapper.vm.showContent).toBeTruthy();
    expect(wrapper.findComponent(Classlist).exists()).toBe(true);
    expect(wrapper.findComponent(ClasslistContent).exists()).toBe(true);
    expect(wrapper.findComponent(CourseStats).exists()).toBe(true);
    expect(wrapper.findComponent(TableView).exists()).toBe(true);

    const section = wrapper.vm.sectionData.sections[0];
    wrapper = mount(ClasslistContent,
      { store,
        localVue,
        propsData: {'section': section, 'isJointSectionDataReady': true}
      });
    await new Promise(setImmediate);
    const link1 = wrapper.findAll('a').at(0);
    expect(link1.text()).toBe('Download (CSV)');
    const link2 = wrapper.findAll('a').at(1);
    expect(link2.text()).toBe('Print');

    wrapper = mount(TableView,
      { store,
        localVue,
        propsData: {'section': section, 'showJointCourseStud': true}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.fields.length).toBe(10);
    expect(wrapper.vm.items.length).toBe(7);
  });

  it('Show data error', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 543}});
    });
    const wrapper = mount(Classlist,
      { store,
        localVue,
        propsData: {'sectionLabel': "2013,autumn,POL S,306/A"}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.dataError).toBeTruthy();
  });

  it('Show no class information', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 404}});
    });
    const wrapper = mount(Classlist,
      { store,
        localVue,
        propsData: {'sectionLabel': "2013,autumn,POL S,306/A"}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.noData).toBeTruthy();
  });
  it('Show no access permission', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 403}});
    });
    const wrapper = mount(Classlist,
      { store,
        localVue,
        propsData: {'sectionLabel': "2013,autumn,POL S,306/A"}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.noAccessPermission).toBeTruthy();
  });
  it('Show invalid course', async () => {
    axios.get.mockImplementation((url) => {
      return Promise.reject({response: {status: 410}});
    });
    const wrapper = mount(Classlist,
      { store,
        localVue,
        propsData: {'sectionLabel': "2013,autumn,POL S,306/A"}
      });
    await new Promise(setImmediate);
    expect(wrapper.vm.invalidCourse).toBeTruthy();
  });
});
