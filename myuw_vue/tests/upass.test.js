import axios from 'axios';
import {mount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import upass from '../vuex/store/upass';
import UpassCard from '../components/accounts/upass.vue';

const localVue = createLocalVue(Vuex);
const mockUpass = {
  "active_employee_membership": true,
  "active_student_membership": true,
  "in_summer": true
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
    expect(wrapper.vm.isActive).toBeTruthy();
    expect(wrapper.vm.employee).toBeFalsy();
    expect(wrapper.vm.student).toBe(true);
    expect(wrapper.vm.seattle).toBe(true);
    expect(wrapper.vm.inSummer).toBeTruthy();
    expect(wrapper.vm.getTroubleshootingUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass#troubleshooting");
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
    expect(wrapper.vm.getTroubleshootingUrl).toBe(
       "mailto:uwbpark@uw.edu?subject=ORCA Question");
    expect(wrapper.vm.getPurchaseUrl).toBe(
      "https://www.uwb.edu/facilities/commuter-services/transportation/upass#Purchase/Cancel%20%20U-Pass");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://www.uwb.edu/facility/commuter-services/transportation/upass#What%20the%20U-PASS%20covers");
  });
  it('Evaluate the computed properties for tac stud', async () => {
    store.state.user.affiliations.tacoma = true;
    store.state.user.affiliations.student = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getTroubleshootingUrl).toBe(
       "https://www.tacoma.uw.edu/fa/facilities/transportation/frequently-asked-questions#permalink-16642");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://www.tacoma.uw.edu/fa/facilities/transportation/u-pass-benefits");
  });
  it('Evaluate the computed properties for pce stud', async () => {
    store.state.user.affiliations.pce = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getTroubleshootingUrl).toBe(
       "https://transportation.uw.edu/getting-here/transit/u-pass#troubleshooting");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
  });

  it('Evaluate the computed properties for employee', async () => {
    store.state.user.affiliations.all_employee = true;
    axios.get.mockResolvedValue({data: mockUpass});
    const wrapper = mount(UpassCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);
    expect(wrapper.vm.getTroubleshootingUrl).toBe(
       "https://transportation.uw.edu/getting-here/transit/u-pass#troubleshooting");
    expect(wrapper.vm.getWhatIsUrl).toBe(
      "https://transportation.uw.edu/getting-here/transit/u-pass");
  });
});
