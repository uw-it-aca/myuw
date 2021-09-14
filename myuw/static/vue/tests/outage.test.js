import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import Outage from '../components/_common/outage.vue';
import stud_schedule from '../vuex/store/schedule/student';
import notices from '../vuex/store/notices';
import profile from '../vuex/store/profile';
import inst_schedule from '../vuex/store/schedule/instructor';
import directory from '../vuex/store/directory';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

const propsData = {
  term: 'current',
};

import mockInstSche from
  './mock_data/inst_schedule/billsea2013spring.json';
import mockEmpProfile from './mock_data/directory/javerage.json';
import mockNotices from './mock_data/notice/javerage.json';
import mockProfile from './mock_data/profile/javg001.json';
import mockStudSche from
  './mock_data/stud_schedule/javerage2013Spring.json';

function generateMockModuleImpl(
  stud_schedule_status,
  notice_status,
  profile_status,
  inst_schedule_status,
  directory_status,
) {
  return (url) => {
    let response = {};
    if (url.includes('/api/v1/schedule/')) {
      response = stud_schedule_status > 400
        ? {status: stud_schedule_status}
        : {data: mockStudSche, status: stud_schedule_status};
    } else if (url.includes('/api/v1/notices/')) {
      response = {data: mockNotices,
                  status: notice_status};
    } else if (url.includes('/api/v1/profile/')) {
      response = {data: mockProfile,
                  status: profile_status};
    } else if (url.includes('/api/v1/directory/')) {
      response = {data: mockEmpProfile,
                  status: directory_status};
    } else if (url.includes('/api/v1/instructor_schedule/')) {
      response = {data: mockInstSche,
                  status: inst_schedule_status};
    }
    if (response.status < 400) {
      return Promise.resolve(response);
    } else {
      return Promise.reject({response});
    }
  };
};

describe('Outage card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        notices,
        profile,
        directory,
        inst_schedule,
      },
      state: {
        user: {
          affiliations: {
            student: true,
            instructor: true,
            all_employee: true,
          }
        }
      },
    });
  });

  it('No error, hide card', async () => {
    axios.get.mockImplementation(generateMockModuleImpl(200, 200, 200, 200, 200));
    const wrapper = mount(Outage, {store, localVue, propsData});
    expect(wrapper.vm.isStudent).toBeTruthy();
    expect(wrapper.vm.isInstructor).toBeTruthy();
    expect(wrapper.vm.isEmployee).toBeTruthy();
    expect(wrapper.vm.scheDataError).toBeFalsy();
    expect(wrapper.vm.noticeDataError).toBeFalsy();
    expect(wrapper.vm.studProfileDataError).toBeFalsy();
    expect(wrapper.vm.studDataError).toBeFalsy();
    expect(wrapper.vm.instDataError).toBeFalsy();
    expect(wrapper.vm.employeeDataError).toBeFalsy();
    expect(wrapper.vm.showOutageCard).toBeFalsy();
  });

  it('api 404, hide card', async () => {
    axios.get.mockImplementation(generateMockModuleImpl(404, 404, 404, 404, 404));
    const wrapper = mount(Outage, {store, localVue, propsData});
    expect(wrapper.vm.isStudent).toBeTruthy();
    expect(wrapper.vm.isInstructor).toBeTruthy();
    expect(wrapper.vm.isEmployee).toBeTruthy();
    expect(wrapper.vm.scheDataError).toBeFalsy();
    expect(wrapper.vm.noticeDataError).toBeFalsy();
    expect(wrapper.vm.studProfileDataError).toBeFalsy();
    expect(wrapper.vm.studDataError).toBeFalsy();
    expect(wrapper.vm.instDataError).toBeFalsy();
    expect(wrapper.vm.employeeDataError).toBeFalsy();
    expect(wrapper.vm.showOutageCard).toBeFalsy();
  });

  it('Show OutageCard if student schedule 543', async () => {
    store.state.user.affiliations.instructor = false;
    store.state.user.affiliations.all_employee = false;
    axios.get.mockImplementation(generateMockModuleImpl(543, 200, 200, 200, 200));
    const wrapper = mount(Outage, {store, localVue, propsData});
    await new Promise(setImmediate);
    expect(wrapper.vm.isInstructor).toBeFalsy();
    expect(wrapper.vm.isEmployee).toBeFalsy();
    expect(wrapper.vm.scheDataError).toBeTruthy();
    expect(wrapper.vm.studDataError).toBeTruthy();
    expect(wrapper.vm.showOutageCard).toBeTruthy();
  });

  it('Show OutageCard if notices 543', async () => {
    store.state.user.affiliations.instructor = false;
    store.state.user.affiliations.all_employee = false;
    axios.get.mockImplementation(generateMockModuleImpl(200, 543, 200, 200, 200));
    const wrapper = mount(Outage, {store, localVue, propsData});
    await new Promise(setImmediate);
    expect(wrapper.vm.isInstructor).toBeFalsy();
    expect(wrapper.vm.isEmployee).toBeFalsy();
    expect(wrapper.vm.noticeDataError).toBeTruthy();
    expect(wrapper.vm.studDataError).toBeTruthy();
    expect(wrapper.vm.showOutageCard).toBeTruthy();
  });

  it('Show OutageCard if profile 543', async () => {
    store.state.user.affiliations.instructor = false;
    store.state.user.affiliations.all_employee = false;
    axios.get.mockImplementation(generateMockModuleImpl(200, 200, 543, 200, 200));
    const wrapper = mount(Outage, {store, localVue, propsData});
    await new Promise(setImmediate);
    expect(wrapper.vm.isInstructor).toBeFalsy();
    expect(wrapper.vm.isEmployee).toBeFalsy();
    expect(wrapper.vm.studProfileDataError).toBeTruthy();
    expect(wrapper.vm.studDataError).toBeTruthy();
    expect(wrapper.vm.showOutageCard).toBeTruthy();
  });

  it('Show OutageCard if employee profile 543', async () => {
    store.state.user.affiliations.instructor = false;
    store.state.user.affiliations.student = false;
    axios.get.mockImplementation(generateMockModuleImpl(404, 404, 404, 200, 543));
    const wrapper = mount(Outage, {store, localVue, propsData});
    await new Promise(setImmediate);
    expect(wrapper.vm.isInstructor).toBeFalsy();
    expect(wrapper.vm.isStudent).toBeFalsy();
    expect(wrapper.vm.employeeDataError).toBeTruthy();
    expect(wrapper.vm.showOutageCard).toBeTruthy();
  });

  it('Show OutageCard if instructor schedule 543', async () => {
    store.state.user.affiliations.student = false;
    axios.get.mockImplementation(generateMockModuleImpl(404, 404, 404, 543, 200));
    const wrapper = mount(Outage, {store, localVue, propsData});
    await new Promise(setImmediate);
    expect(wrapper.vm.isStudent).toBeFalsy();
    expect(wrapper.vm.instDataError).toBeTruthy();
    expect(wrapper.vm.showOutageCard).toBeTruthy();
  });
});
