import axios from 'axios';
import { shallowMount, createLocalVue } from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import Notices from '../store/notices';
import NewStudentCard from '../components/index/cards/international/new-student.vue';
import StudentCard from '../components/index/cards/international/student.vue';
import SeattleComp from '../components/index/cards/international/seattle.vue';
import BothellComp from '../components/index/cards/international/bothell.vue';
import TacomaComp from '../components/index/cards/international/tacoma.vue';
import UwCard from '../containers/card.vue';

import mockNotices from './mock_data/inter_notices.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

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

  it('Render Logic intl_stud = true', () => {
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
  });

  it('Render Logic intl_stud = false', () => {
    store.state.user.affiliations.intl_stud = false;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Render Logic seattle = true', () => {
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(true);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic bothell = true', () => {
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.bothell = true;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(true);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(false);
  });

  it('Render Logic tacoma = true', () => {
    store.state.user.affiliations.seattle = false;
    store.state.user.affiliations.tacoma = true;
    const wrapper = shallowMount(StudentCard, { store, localVue });
    expect(wrapper.findComponent(SeattleComp).exists()).toBe(false);
    expect(wrapper.findComponent(BothellComp).exists()).toBe(false);
    expect(wrapper.findComponent(TacomaComp).exists()).toBe(true);
  });

  it('Render Logic all campus false', () => {
    store.state.user.affiliations.seattle = false;
    const wrapper = shallowMount(StudentCard, { store, localVue });
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
    ).toBe('http://www.uwb.edu/cie/current-students/travel');
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
    ).toBe('http://www.tacoma.uw.edu/iss/travel-visas');
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
    await new Promise((r) => setTimeout(r, 10));

    expect(
      Notices.getters.isReady(wrapper.vm.$store.state.notices),
    ).toBeTruthy();
    expect(
      Notices.getters.isErrored(wrapper.vm.$store.state.notices),
    ).toBeFalsy();

    expect(wrapper.vm.notices).toHaveLength(1);
    expect(wrapper.findAll('div')).toHaveLength(1);
    // The html retuned from uw is a improper, it does not have the
    // closing span tag.
    expect(
      wrapper.findAll('div').at(0).html()
    ).toBe('<div>' + mockNotices[23].notice_body + '</span></div>');
  });
});