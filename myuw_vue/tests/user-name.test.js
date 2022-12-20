import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import directory from '../vuex/store/directory';
import Uname from '../components/profile/user-name.vue';

const localVue = createLocalVue(Vuex);
const mockData = {
  "full_name": "JAMES AVERAGE STUDENT",
  "display_name": "J. Average Student",
};
const mockData1 = {
  "full_name": "JAMES AVERAGE STUDENT",
   "display_name": "JAMES AVERAGE STUDENT",
};
jest.mock('axios');

describe('Uname Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        directory,
      },
    });
  });

  it('Having diff pref name and full name specified', async () => {
    axios.get.mockResolvedValue({data: mockData});
    const wrapper = mount(Uname, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.hasName).toBe(true);
    expect(wrapper.vm.name).toBe("J. Average Student");
  });
  it('Pref name is the same as full name', async () => {
    axios.get.mockResolvedValue({data: mockData1});
    const wrapper = mount(Uname, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBe(true);
    expect(wrapper.vm.hasName).toBe(true);
    expect(wrapper.vm.name).toBe("JAMES AVERAGE STUDENT");
  });
});
