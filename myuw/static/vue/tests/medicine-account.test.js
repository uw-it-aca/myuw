import axios from 'axios';

import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
library.add(faExclamationTriangle);

import { mount } from '@vue/test-utils';
import { createLocalVue } from './helper';

import Vuex from 'vuex';
import profile from '../vuex/store/profile';

import UwCard from '../components/_templates/card.vue';
import MedicineAccountCard from '../components/accounts/medicine-account.vue';
import mockJinterProfile from './mock_data/profile/jinter.json';

const localVue = createLocalVue(Vuex);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('uw-card', UwCard);

jest.mock('axios');

describe('Husky Card', () => {
  let store;

  beforeEach(() => {
    store = new Vuex.Store({
      modules: {
        profile,
      },
      state: {
        staticUrl: '/static/',
      }
    });
  });

  it('Hide card if no active med password', async () => {
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, {store, localVue});
    await new Promise((r) => setTimeout(r, 10));
    expect(wrapper.vm.showCard).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Show card, password expired', async () => {
    mockJinterProfile.password.has_active_med_pw = true;
    mockJinterProfile.password.med_pw_expired = true;
    mockJinterProfile.password.expires_med = '2013-04-01 00:00:00-08:00';
    mockJinterProfile.password.days_before_med_pw_expires = undefined;
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise((r) => setTimeout(r, 10));
    
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.hasActiveMedPw).toBe(true);
    expect(wrapper.vm.medPwExpired).toBe(true);
    expect(wrapper.vm.expiresMed).toBe('2013-04-01 00:00:00-08:00');
    expect(wrapper.vm.daysPwExpires).toBe(undefined);

    expect(wrapper.vm.toFriendlyDate(wrapper.vm.expiresMed)).toBe('Mon, Apr 1');
    expect(wrapper.vm.expires30Days).toBe(false);
  });

  it('Show card, password not expired', async () => {
    mockJinterProfile.password.has_active_med_pw = true;
    mockJinterProfile.password.med_pw_expired = false;
    mockJinterProfile.password.expires_med = '2013-06-03 10:57:06-08:00';
    mockJinterProfile.password.days_before_med_pw_expires = 49;
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise((r) => setTimeout(r, 10));
    
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.hasActiveMedPw).toBe(true);
    expect(wrapper.vm.medPwExpired).toBe(false);
    expect(wrapper.vm.expiresMed).toBe('2013-06-03 10:57:06-08:00');
    expect(wrapper.vm.daysBeforeExpires).toBe(49);

    expect(wrapper.vm.toFriendlyDate(wrapper.vm.expiresMed)).toBe('Mon, Jun 3');
    expect(wrapper.vm.expires30Days).toBe(false);
  });

  it('toFriendlyDate', () => {
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, {store, localVue});

    expect(
      wrapper.vm.toFriendlyDate('2020-08-24')
    ).toEqual('Mon, Aug 24');

    expect(
      wrapper.vm.toFriendlyDate(undefined)
    ).toEqual('');
    expect(
      wrapper.vm.toFriendlyDate('')
    ).toEqual('');
  });
});
