import axios from 'axios';
import dayjs from 'dayjs';
import {mount, shallowMount} from '@vue/test-utils';
import {createLocalVue, expectAction} from './helper';
import {statusOptions} from '../vuex/store/model_builder';
import Vuex from 'vuex';
import events from '../vuex/store/events';
import EventsCard from '../components/pages/home/cards/events/events.vue';
import ListEvents from '../components/pages/home/cards/events/list-events.vue';

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
    axios.get.mockResolvedValue({data: mockEvents, status: 200});
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
    };
    return expectAction(events.actions.fetch, null, events.state, getters, [
      {type: 'setStatus', payload: statusOptions[1]},
      {type: 'setValue', payload: mockEvents},
      {type: 'setStatus', payload: statusOptions[0]},
    ]);
  });

  it('Check status changes on fetch - failure', () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const getters = {
      isReadyTagged: () => false,
      isFetchingTagged: () => false,
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

  it('Basic Render', () => {
    axios.get.mockResolvedValue({data: mockEvents, status: 200});
    const wrapper = shallowMount(EventsCard, {store, localVue});

    expect(wrapper.find('h3').text()).toEqual('Events');
  });

  it('acalDateFormat', () => {
    axios.get.mockResolvedValue({data: mockEvents, status: 200});
    const wrapper = mount(ListEvents, {
      store, 
      localVue,
      propsData: {
        events: [],
      }
    });

    expect(
      wrapper.vm.acalDateFormat(dayjs('2020-08-19'), dayjs('2020-08-19'))
    ).toEqual('August 19');
    expect(
      wrapper.vm.acalDateFormat(dayjs('2020-08-19'), dayjs('2020-08-20'))
    ).toEqual('August 19 - 20');
  });

  it('Future Cal Render', () => {
    axios.get.mockResolvedValue({
      data: { 'future_active_cals': mockEvents['future_active_cals'] },
      status: 200,
    });
    const wrapper = shallowMount(EventsCard, {store, localVue});

    expect(wrapper.find('h3').text()).toEqual('Events');
  });
});
