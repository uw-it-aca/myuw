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
            student: false,
            pce: false,
            seattle: false,
            bothell: false,
            tacoma: false,
            all_employee: false,
          }
        }
      }
    });
  });

  it('Evaluate the computed properties for sea stud', async () => {
    store.state.user.affiliations.seattle = true;
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.isCurrent).toBeFalsy();
    expect(wrapper.vm.employee).toBeFalsy();
    expect(wrapper.vm.student).toBe(true);
    expect(wrapper.vm.seattle).toBe(true);
    expect(wrapper.vm.inSummer).toBeTruthy();
    expect(wrapper.vm.displayActivation).toBeTruthy();
    expect(wrapper.vm.getUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
  });
  it('Evaluate the computed properties for bot stud', async () => {
    store.state.user.affiliations.bothell = true;
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getUrl).toBe(
       "https://www.uwb.edu/facility/commuter-services/upass");
    expect(wrapper.vm.getPurchaseUrl).toBe(
      "https://www.uwb.edu/facility/commuter-services/upass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://www.uwb.edu/facility/commuter-services/upass");
  });
  it('Evaluate the computed properties for tac stud', async () => {
    store.state.user.affiliations.tacoma = true;
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getUrl).toBe(
       "https://www.tacoma.uw.edu/getting-campus/u-pass-orca");
    expect(wrapper.vm.getPurchaseUrl).toBe(
      "https://www.tacoma.uw.edu/getting-campus/students-purchasing-u-pass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://www.tacoma.uw.edu/getting-campus/what-u-pass");
  });
  it('Evaluate the computed properties for pce stud', async () => {
    store.state.user.affiliations.pce = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getUrl).toBe(
       "https://transportation.uw.edu/getting-here/transit/u-pass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
  });

  it('Evaluate the computed properties for employee', async () => {
    store.state.user.affiliations.all_employee = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getUrl).toBe(
       "https://transportation.uw.edu/getting-here/transit/u-pass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
  });
});
