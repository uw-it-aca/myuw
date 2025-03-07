import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import idcard from '../vuex/store/idcard-elig';
import IDcardCard from '../components/accounts/idcard.vue';

const localVue = createLocalVue(Vuex);
const mockIDcard = {
  "not_eligible": false, "employee_eligible": false,
  "retiree_eligible": true, "student_eligible": true
};

jest.mock('axios');

describe('IDcard Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        idcardelig,
      },
      state: {
        user: {
          affiliations: {
            student: true,
            retiree: true,
            employee: false,
            past_employee: false,
            past_stud: false,
          }
        }
      }
    });
  });

  it('Evaluate the computed properties', async () => {
    axios.get.mockResolvedValue({data: mockIDcard});
    const wrapper = mount(IDcardCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isTargetViewer).toBeTruthy();
    expect(wrapper.vm.employee).toBeFalsy();
    expect(wrapper.vm.student).toBe(true);
    expect(wrapper.vm.past_employee).toBeFalsy();
    expect(wrapper.vm.past_stud).toBeFalsy();
    expect(wrapper.vm.retiree).toBeTruthy();
    expect(wrapper.vm.showCard).toBeTruthy();
    expect(wrapper.vm.idcard).toBeTruthy();
  });
  it('Show custom error msg for 543', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = shallowMount(IDcardCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.showError).toBeTruthy();
  });
});
