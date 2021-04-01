import axios from 'axios';
import { mount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import ApplicantModel from '../vuex/store/applicant';
import ApplicantCard from '../components/home/applicant/applicant.vue';
import SeattleComp from '../components/home/applicant/seattle.vue';
import BothellComp from '../components/home/applicant/bothell.vue';
import TacomaComp from '../components/home/applicant/tacoma.vue';
import UwCard from '../components/_templates/card.vue';

import mockApplicant from './mock_data/applicant.json';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Applicant Card - applicant.vue', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'applicant': ApplicantModel,
      },
      state: {
        user: {
          affiliations: {
            applicant: true,
          }
        }
      }
    });
  });

  it('Render Logic applicant = true', async () => {
    axios.get.mockResolvedValue({data: mockApplicant});
    const wrapper = mount(ApplicantCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.find('div').exists()).toBe(true);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(true);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(true);
    expect(wrapper.vm.seattleApplicant.is_seattle).toBe(true);
    expect(wrapper.vm.bothellApplicant.is_bothell).toBe(true);
    expect(wrapper.vm.tacomaApplicant.is_tacoma).toBe(true);
  });

  it('Render Logic applicant = false', async () => {
    store.state.user.affiliations.applicant = false;
    axios.get.mockResolvedValue({data: mockApplicant});
    const wrapper = mount(ApplicantCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.find('div').exists()).toBe(false);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic no campus', async () => {
    axios.get.mockResolvedValue({data: []});
    const wrapper = mount(ApplicantCard, { store, localVue });
    // It takes like 10 ms for the dom to update
    await new Promise(setImmediate);
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(SeattleComp).findComponent(UwCard).exists()
    ).toBe(false);
    expect(
      wrapper.findComponent(TacomaComp).findComponent(UwCard).exists()
    ).toBe(false);
  });
});
