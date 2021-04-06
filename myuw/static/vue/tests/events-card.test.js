import axios from 'axios';
import dayjs from 'dayjs';
import {mount, shallowMount} from '@vue/test-utils';
import {createLocalVue, expectAction} from './helper';
import {statusOptions} from '../vuex/store/model_builder';
import Vuex from 'vuex';
import events from '../vuex/store/events';
import EventsCard from '../components/home/events/events.vue';
import ListEvents from '../components/home/events/list-events.vue';

import {
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';

import mockEvents from './mock_data/events.json';

const localVue = createLocalVue(Vuex);

localVue.component('font-awesome-layers', FontAwesomeLayers);

jest.mock('axios');

describe('Event Store and Card', () => {
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

  it('Hide card when no data', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 404}}));
    const wrapper = shallowMount(EventsCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.statusCode).toBe(404);
    expect(wrapper.vm.isReady).toBe(false);
    expect(wrapper.vm.showError).toBe(false);
  });

  it('Show error', async () => {
    axios.get.mockResolvedValue(Promise.reject({response: {status: 543}}));
    const wrapper = shallowMount(EventsCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.isErrored).toBe(true);
    expect(wrapper.vm.statusCode).toBe(543);
    expect(wrapper.vm.isReady).toBe(false);
    expect(wrapper.vm.showError).toBe(true);
  });

  it('Basic Render', async () => {
    axios.get.mockResolvedValue({data: mockEvents, status: 200});
    const wrapper = mount(EventsCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.shownEvents.length).toBe(6);
    expect(wrapper.vm.futureCalCount).toBe(3);
    expect(wrapper.vm.futureCalLinks.length).toBe(1);
    expect(wrapper.vm.hiddenEvents.length).toBe(1);
    expect(wrapper.find('h2').text()).toEqual('Events');
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

    expect(wrapper.find('h2').text()).toEqual('Events');
  });
});
