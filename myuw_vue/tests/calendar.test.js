import axios from 'axios';
import dayjs from 'dayjs';

import { shallowMount } from '@vue/test-utils';
import { createLocalVue, deepClone } from './helper';

import Vuex from 'vuex';
import academic_events from '../vuex/store/academic_events';

import mockEventFaculty20210701 from
  './mock_data/academic_events/acad_events_faulty.json';
import mockEventsStud20210928 from
  './mock_data/academic_events/acad_events_stud.json';

import UwCard from '../components/_templates/card.vue';
import AcadCalTabs from '../components/calendar/tabs.vue';
import AcadCalCards from '../components/calendar/calendar-cards.vue';
import UwTabs from '../components/_templates/tabs/tabs.vue';
import UwTab from '../components/_templates/tabs/tab.vue';

const localVue = createLocalVue(Vuex);

jest.mock('axios');

describe('Academic Calendar Page Content', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        academic_events,
      },
    });
  });

  it('Faculty Content', async () => {
    axios.get.mockResolvedValue({data: mockEventFaculty20210701, status: 200});
    let wrapper = shallowMount(AcadCalTabs, { store, localVue });
    await new Promise(setImmediate);

    expect(wrapper.findComponent(UwTabs).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwTab).length).toBe(2);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.vm.allEvents.length).toBe(93);
    expect(wrapper.vm.breakEvents.length).toBe(16);

    const allEvents = wrapper.vm.allEvents;
    expect(wrapper.vm.allEvents[0].year).toBe("2021");
    expect(wrapper.vm.allEvents[0].label).toBe(
      "2021 Summer, Registration Period 2 - Autumn Quarter"
    );
    expect(wrapper.vm.allEvents[0].start).toEqual(dayjs("2021-06-21"));
    expect(wrapper.vm.allEvents[0].end).toEqual(dayjs("2021-09-28"));
    const breakEvents = wrapper.vm.breakEvents;
  
    wrapper = shallowMount(AcadCalCards, {store, localVue,
      propsData: {'events': allEvents}});
    await new Promise(setImmediate);
    expect(wrapper.findComponent(AcadCalCards).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCard).length).toBe(6);

    wrapper = shallowMount(AcadCalCards, {store, localVue,
      propsData: {'events': breakEvents}});
    await new Promise(setImmediate);
    expect(wrapper.findComponent(AcadCalCards).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCard).length).toBe(5);
  });

  it('Student Content', async () => {
    axios.get.mockImplementation((url) => {
      const urlData = {
        '/api/v1/academic_events/': deepClone(mockEventsStud20210928),
      };
      return Promise.resolve({data: urlData[url]});
    });
    let wrapper = shallowMount(AcadCalTabs, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.isReady).toBeTruthy();
    expect(wrapper.findComponent(AcadCalTabs).exists()).toBe(true);
    expect(wrapper.vm.allEvents.length).toBe(27);
    expect(wrapper.vm.breakEvents.length).toBe(14);
    const allEvents = wrapper.vm.allEvents;
    const breakEvents = wrapper.vm.breakEvents;

    wrapper = shallowMount(AcadCalCards, {store, localVue,
      propsData: {'events': allEvents}});
    await new Promise(setImmediate);
    expect(wrapper.findComponent(AcadCalCards).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCard).length).toBe(4);

    wrapper = shallowMount(AcadCalCards, {store, localVue,
      propsData: {'events': breakEvents}});
    await new Promise(setImmediate);
    expect(wrapper.findComponent(AcadCalCards).exists()).toBe(true);
    expect(wrapper.findAllComponents(UwCard).length).toBe(4);
  });
});
