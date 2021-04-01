import axios from 'axios';

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import storeLibrary from '../vuex/store/library';

import UwCard from '../components/_templates/card.vue';
import LibraryCard from '../components/accounts/library.vue';

let mockRes = {
  holds_ready: 1,
  fines: 0,
  items_loaned: 1,
  next_due: '2014-05-27T02:00:00+00:00',
};

const localVue = createLocalVue(Vuex);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Library Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        'library': storeLibrary,
      },
    });
  });

  it('Testing mapped state', async () => {
    axios.get.mockResolvedValue({data: mockRes, status: 200});
    const wrapper = mount(LibraryCard, { store, localVue });
    await new Promise((r) => setTimeout(r, 10));

    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.holdsReady).toBe(1);
    expect(wrapper.vm.fines).toBe(0);
    expect(wrapper.vm.itemsLoaned).toBe(1);
    expect(wrapper.vm.nextDue).toBe('2014-05-27T02:00:00+00:00');
  });

  it('isPlural', () => {
    axios.get.mockResolvedValue({data: mockRes, status: 200});
    const wrapper = mount(LibraryCard, {store, localVue});

    expect(wrapper.vm.isPlural(1)).toBeFalsy();
    expect(wrapper.vm.isPlural(2)).toBeTruthy();
    expect(wrapper.vm.isPlural(0)).toBeTruthy();
  });
});
