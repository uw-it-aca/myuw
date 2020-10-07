import axios from 'axios';
import { mount, shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import ApplicantModel from '../vuex/store/applicant';
import ApplicantCard from '../components/index/cards/applicant/applicant.vue';
import SeattleComp from '../components/index/cards/applicant/seattle.vue';
import BothellComp from '../components/index/cards/applicant/bothell.vue';
import TacomaComp from '../components/index/cards/applicant/tacoma.vue';
import UwCard from '../layouts/card.vue';

import mockApplicant from './mock_data/applicant.json';

const localVue = createLocalVue();

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
    const wrapper = shallowMount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(true);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(true);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(true);
  });

  it('Render Logic applicant = false', async () => {
    store.state.user.affiliations.applicant = false;
    axios.get.mockResolvedValue({data: mockApplicant});
    const wrapper = shallowMount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(false);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic all campus', async () => {
    axios.get.mockResolvedValue({data: mockApplicant});
    const wrapper = mount(ApplicantCard, { store, localVue });
    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(SeattleComp).findComponent(UwCard).exists()
    ).toBe(true);
    expect(
      wrapper.findComponent(BothellComp).findComponent(UwCard).exists()
    ).toBe(true);
    expect(
      wrapper.findComponent(TacomaComp).findComponent(UwCard).exists()
    ).toBe(true);
  });

  it('Render Logic no campus', async () => {
    axios.get.mockResolvedValue({data: []});
    const wrapper = mount(ApplicantCard, { store, localVue });
    // It takes like 10 ms for the dom to update
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(SeattleComp).findComponent(UwCard).exists()
    ).toBe(false);
    expect(
      wrapper.findComponent(BothellComp).findComponent(UwCard).exists()
    ).toBe(false);
    expect(
      wrapper.findComponent(TacomaComp).findComponent(UwCard).exists()
    ).toBe(false);
  });
});

describe('Applicant Card - seattle.vue', () => {
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

  it('Render Logic seattle only', async () => {
    axios.get.mockResolvedValue({data: [mockApplicant[1]]});
    const wrapper = mount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(SeattleComp).findComponent(UwCard).exists()
    ).toBe(true);
  });

  it('Render Logic not seattle', async () => {
    axios.get.mockResolvedValue({
      data: [mockApplicant[0], mockApplicant[2]],
    });
    const wrapper = shallowMount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(SeattleComp).findComponent(UwCard).exists()
    ).toBe(false);
  });
});

describe('Applicant Card - bothell.vue', () => {
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

  it('Render Logic seattle only', async () => {
    axios.get.mockResolvedValue({data: [mockApplicant[0]]});
    const wrapper = mount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(BothellComp).findComponent(UwCard).exists()
    ).toBe(true);
  });

  it('Render Logic not seattle', async () => {
    axios.get.mockResolvedValue({
      data: [mockApplicant[1], mockApplicant[2]],
    });
    const wrapper = shallowMount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(BothellComp).findComponent(UwCard).exists()
    ).toBe(false);
  });
});

describe('Applicant Card - tacoma.vue', () => {
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

  it('Render Logic seattle only', async () => {
    axios.get.mockResolvedValue({data: [mockApplicant[2]]});
    const wrapper = mount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(TacomaComp).findComponent(UwCard).exists()
    ).toBe(true);
  });

  it('Render Logic not seattle', async () => {
    axios.get.mockResolvedValue({
      data: [mockApplicant[0], mockApplicant[1]],
    });
    const wrapper = shallowMount(ApplicantCard, { store, localVue });
    expect(wrapper.find('div').exists()).toBe(true);
    expect(
      wrapper.findComponent(TacomaComp).findComponent(UwCard).exists()
    ).toBe(false);
  });
});