import axios from 'axios';
import {mount, shallowMount} from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import grad from '../vuex/store/grad';
import GradStatusCard from '../components/academics/grad-status.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
} from '@fortawesome/vue-fontawesome';
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

import mockGradData from './mock_data/sea_grad.json';

const localVue = createLocalVue(Vuex);

library.add(faExclamationTriangle);

localVue.component('font-awesome-icon', FontAwesomeIcon);

jest.mock('axios');

describe('Grad Status Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        grad,
      },
      state: {
        user: {
          affiliations: {
            grad: true,
          }
        }
      }
    });
  });

  it('Check status changes on fetch', async () => {
    axios.get.mockResolvedValue({data: mockGradData, status: 200});
    const wrapper = shallowMount(GradStatusCard, {store, localVue});
    expect(
        grad.getters.isFetching(wrapper.vm.$store.state.grad),
    ).toBeTruthy();
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(
        grad.getters.isReady(wrapper.vm.$store.state.grad),
    ).toBeTruthy();
    expect(
        grad.getters.isErrored(wrapper.vm.$store.state.grad),
    ).toBeFalsy();
    expect(
        grad.getters.statusCode(wrapper.vm.$store.state.grad),
    ).toEqual(200);
  });

  it('Check data parsing and header rendering', async () => {
    axios.get.mockResolvedValue({data: mockGradData, status: 200});
    const wrapper = mount(GradStatusCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.isReady).toBeTruthy();

    expect(wrapper.vm.petitions).toHaveLength(7);
    expect(wrapper.vm.leaves).toHaveLength(3);
    expect(wrapper.vm.degrees).toHaveLength(8);
    expect(wrapper.findAll('h4')).toHaveLength(3);
  });

  it('Show custom error msg for 543', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = mount(GradStatusCard, {store, localVue});
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise((r) => setTimeout(r, 10));
    
    expect(wrapper.vm.showError).toBeTruthy();
    expect(wrapper.findAll('a')).toHaveLength(1);
  });
});
