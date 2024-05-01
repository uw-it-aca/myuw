import axios from 'axios';
import { mount, shallowMount } from '@vue/test-utils';
import Vuex from 'vuex';
import {createLocalVue} from './helper';
import Notices from '../vuex/store/notices';
import NewStudentCard from '../components/home/international/new-student.vue';
import StudentCard from '../components/home/international/student.vue';
import SeattleComp from '../components/home/international/seattle.vue';
import BothellComp from '../components/home/international/bothell.vue';
import TacomaComp from '../components/home/international/tacoma.vue';
import UwCard from '../components/_templates/card.vue';
import Tabs from '../components/_templates/tabs/tabs.vue';
import TabButton from '../components/_templates/tabs/button.vue';
import TabPanel from '../components/_templates/tabs/panel.vue';

import mockNotices from './mock_data/notice/jinter.json';

const localVue = createLocalVue(Vuex);

describe('International Student Card - student.vue', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            intl_stud: true,
            F1: true,
            seattle: true,
            bothell: false,
            tacoma: false,
          }
        }
      }
    });
  });

  it('Render Logic intl student', () => {
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });

  it('Render Logic not intl student', () => {
    store.state.user.affiliations.intl_stud = false;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Render Logic seattle intl student', () => {
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.vm.seattle).toBe(true);
    expect(wrapper.vm.bothell).toBe(false);
    expect(wrapper.vm.tacoma).toBe(false);
    expect(wrapper.vm.singleCampus).toBe(true);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(true);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic bothell intl student', () => {
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.bothell = true;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.vm.singleCampus).toBe(true);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(true);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic tacoma intl student', () => {
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.tacoma = true;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.vm.singleCampus).toBe(true);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(true);
  });

  it('Render Logic for no campus', () => {
    store.state.user.affiliations.seattle = false;
    const wrapper = mount(StudentCard, { store, localVue });
    expect(wrapper.vm.singleCampus).toBe(false);
    expect(wrapper.vm.noCampus).toBe(true);
    expect(wrapper.findComponent(Tabs).exists()).toBe(true);
    expect(wrapper.findAllComponents(TabButton).length).toBe(3);
    expect(wrapper.findAllComponents(TabPanel).length).toBe(3);
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(true);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(true);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(true);
  });
});

describe('International Student Components - seattle.vue', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            intl_stud: true,
            J1: true,
            seattle: true,
            bothell: false,
            tacoma: false,
          }
        }
      }
    });
  });

  it('Render Logic J1', () => {
    const wrapper = shallowMount(SeattleComp, { store, localVue });
    expect(
      wrapper.findAll('a').at(1).text()
    ).toBe('Visa and Immigration Rules for J-1 students');
  });

  it('Render Logic F1', () => {
    store.state.user.affiliations.J1 = false;
    const wrapper = shallowMount(SeattleComp, { store, localVue });
    expect(
      wrapper.findAll('a').at(1).text()
    ).toBe('Visa and Immigration Rules for F-1 students');
  });
});

describe('International Student Components - bothell.vue', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            intl_stud: true,
            J1: true,
            seattle: false,
            bothell: true,
            tacoma: false,
          }
        }
      }
    });
  });

  it('Check url', () => {
    const wrapper = shallowMount(BothellComp, { store, localVue });
    expect(
      wrapper.findAll('a').at(0).attributes().href
    ).toBe('https://www.uwb.edu/international-student-services/');
  });
});

describe('International Student Card - tacoma.vue', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      state: {
        user: {
          affiliations: {
            intl_stud: true,
            J1: true,
            seattle: true,
            bothell: false,
            tacoma: false,
          }
        }
      }
    });
  });

  it('Check url', () => {
    const wrapper = shallowMount(TacomaComp, { store, localVue });
    expect(
      wrapper.findAll('a').at(0).attributes().href
    ).toBe('https://www.tacoma.uw.edu/uwt/oga/isss-travel-and-visa');
  });
});

jest.mock('axios');

describe('New International Student Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        "notices": Notices,
      },
      state: {
        user: {
          affiliations: {
            intl_stud: true,
          }
        }
      }
    });
  });

  it('Check url', async () => {
    axios.get.mockResolvedValue({data: mockNotices, status: 200});
    const wrapper = shallowMount(NewStudentCard, { store, localVue });
    // It takes like 10 ms to process the mock data through fetch postProcess
    await new Promise(setImmediate);

    expect(
      Notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
      Notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeFalsy();

    expect(wrapper.vm.notices).toHaveLength(1);
  });
});