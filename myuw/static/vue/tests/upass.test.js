import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import upass from '../vuex/store/upass';
import UpassCard from '../components/accounts/upass.vue';

const localVue = createLocalVue(Vuex);
const mockUpass = {
  "status_message": "b\"<p><span class='highlight'>Your U-PASS is not current.</span></p><p><a href='http://www.washington.edu/u-pass'>Learn more</a> about U-PASS program member benefits.</p>\\n\"",
  "is_current": false,
  "is_employee": false,
  "is_student": true,
  "in_summer": true,
  "display_activation": true,
};

jest.mock('axios');

describe('Upass Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        upass,
      },
      state: {
        user: {
          affiliations: {
            student: true,
          }
        }
      }
    });
  });

  it('Evaluate the computed properties', async () => {
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.is_current).toBeFalsy();
    expect(wrapper.vm.is_employee).toBeFalsy();
    expect(wrapper.vm.in_summer).toBeTruthy();
    expect(wrapper.vm.display_activation).toBeTruthy();
  });
});
