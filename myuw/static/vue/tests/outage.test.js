import axios from 'axios';
import {shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import Outage from '../components/_common/outage.vue';
import stud_schedule from '../vuex/store/schedule/student';
import notices from '../vuex/store/notices';
import profile from '../vuex/store/profile';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

const propsData = {
  term: 'current',
};

const modules = {
  stud_schedule,
  notices,
  profile,
};

function generateMockModuleImpl(
  stud_schedule_status,
  notice_status,
  profile_status,
) {
  return (url) => {
    let response = {};
    if (url.includes('/api/v1/schedule/')) {
      response = {data: {sections: []}, status: stud_schedule_status};
    } else if (url.includes('/api/v1/notices/')) {
      response = {data: [], status: notice_status};
    } else if (url.includes('/api/v1/profile/')) {
      response = {data: [], status: profile_status};
    }

    if (response.status < 400) {
      return Promise.resolve(response);
    } else {
      return Promise.reject({response});
    }
  };
}

describe('Outage card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        stud_schedule,
        notices,
        profile,
      },
      state: {
        user: {
          affiliations: {
            student: true,
            instructor: false,
            employee: false,
          }
        }
      },
    });
  });


  it('non404Error checking', () => {
    axios.get.mockImplementation(generateMockModuleImpl(200, 200, 200));
    const wrapper = shallowMount(Outage, {store, localVue, propsData});
    expect(wrapper.vm.non404Error(200)).toBeFalsy();
    expect(wrapper.vm.non404Error(404)).toBeFalsy();
    expect(wrapper.vm.non404Error(543)).toBeTruthy();
    expect(wrapper.vm.non404Error(400)).toBeTruthy();
  });

  describe('showOutageCard for Student', () => {
    let store;

    beforeEach(() => {
      store = new Vuex.Store({
        modules: {
          stud_schedule,
          notices,
          profile,
        },
        state: {
          user: {
            affiliations: {
              student: true,
              instructor: false,
              employee: false,
            }
          }
        },
      });
    });

    it('showOutageCard for Student - Successful calls', () => {
      axios.get.mockImplementation(generateMockModuleImpl(200, 200, 200));

      const wrapper = shallowMount(Outage, {store, localVue, propsData});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 404 Error', () => {
      axios.get.mockImplementation(generateMockModuleImpl(404, 200, 200));
  
      const wrapper = shallowMount(Outage, {store, localVue, propsData});
      expect(wrapper.vm.showOutageCard).toBeFalsy();
    });

    it('showOutageCard for Student - 543 Error', async () => {
      axios.get.mockImplementation(generateMockModuleImpl(543, 200, 200));
    
      const wrapper = shallowMount(Outage, {store, localVue, propsData});
      await new Promise((r) => setTimeout(r, 10));
      expect(wrapper.vm.showOutageCard).toBeTruthy();
    });
  });
  // TODO: Add tests for the instructor and employee status'
  // This currently only tests for the case of a student.

});