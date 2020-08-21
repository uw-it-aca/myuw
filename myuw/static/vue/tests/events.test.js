import axios from 'axios';
import moment from 'moment';
import {mount, shallowMount, createLocalVue} from '@vue/test-utils';
import {expectAction} from './helper';
import {statusOptions} from '../store/model_builder';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';
import events from '../store/events';
import EventsCard from '../components/index/cards/events/events.vue';
import ListEvents from '../components/index/cards/events/list-events.vue';

import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

import {
  faExclamationTriangle,
  faLocationArrow
} from '@fortawesome/free-solid-svg-icons';

import mockEvents from './mock_data/events.json';

const localVue = createLocalVue();
localVue.use(BootstrapVue);
localVue.use(Vuex);

library.add(faExclamationTriangle);
library.add(faLocationArrow);

localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Event Store', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'events': events,
      },
    });
  });

  it('Check status changes on fetch - success', () => {
    axios.get.mockResolvedValue({data: mockEvents});
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(events.actions.fetch, null, events.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockEvents},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject(new Error('Test Reject')));
    const getters = {
      isReady: false,
      isFeatching: false,
    };
    return expectAction(events.actions.fetch, null, events.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setStatus', payload: statusOptions[2]},
    ]);
  });
});

describe('Events Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'events': events,
      },
    });
  });

  it('Basic Render', async () => {
    axios.get.mockResolvedValue({data: mockEvents});
    const wrapper = mount(EventsCard, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').text()).toEqual('Events');
  });

  it('acalDateFormat', async () => {
    axios.get.mockResolvedValue({data: mockEvents});
    const wrapper = mount(ListEvents, {
      store, 
      localVue,
      propsData: {
        events: [],
      }
    });

    await new Promise((r) => setTimeout(r, 10));
    expect(
      wrapper.vm.acalDateFormat(moment('2020-08-19'), moment('2020-08-19'))
    ).toEqual('August 19');
    expect(
      wrapper.vm.acalDateFormat(moment('2020-08-19'), moment('2020-08-20'))
    ).toEqual('August 19 - 20');
  });

  it('Future Cal Render', async () => {
    axios.get.mockResolvedValue({
      data: { 'future_active_cals': mockEvents['future_active_cals'] }
    });
    const wrapper = mount(EventsCard, {store, localVue});

    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.find('h3').text()).toEqual('Events');
  });
});
