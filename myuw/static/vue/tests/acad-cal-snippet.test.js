import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { shallowMount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import academic_events from '../vuex/store/academic_events';

import UwCard from '../components/_templates/card.vue';
import AcadCalSnippet from '../components/home/calendar/acad-cal-snippet.vue';

import facultyAcadEvents from './mock_data/academic_events/faculty.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Academic Calendar Snippet', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        academic_events,
      },
      state: {
        user: {
          affiliations: {
            instructor: true,
          },
        },
      },
    });
  });

  it('Computed Properties', async () => {
    axios.get.mockResolvedValue({data: facultyAcadEvents, status: 200});
    const wrapper = shallowMount(AcadCalSnippet, { store, localVue });
    await new Promise(setImmediate);

    expect(wrapper.vm.events.length).toBe(4);
    expect(wrapper.vm.instructor).toBeTruthy();
    expect(wrapper.vm.showCard).toBeTruthy();
  });

  it('formatBannerDate()', async () => {
    axios.get.mockResolvedValue({data: facultyAcadEvents, status: 200});
    const wrapper = shallowMount(AcadCalSnippet, {store, localVue});
    await new Promise(setImmediate);

    let multiDayEvent = wrapper.vm.events[0];
    let oneDayEvent = wrapper.vm.events[1];

    expect(wrapper.vm.formatBannerDate(multiDayEvent)).toBe('Apr 10 - Apr 24');
    expect(wrapper.vm.formatBannerDate(oneDayEvent)).toBe('Apr 15 (Monday)');
  });
});
