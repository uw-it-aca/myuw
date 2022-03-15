import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import axios from 'axios';
import { mount } from '@vue/test-utils';
import Vuex from 'vuex';
import { createLocalVue } from './helper';
import profile from '../vuex/store/profile';
import UwCard from '../components/_templates/card.vue';
import MedicineAccountCard from '../components/accounts/medicine-account.vue';
import mockJinterProfile from './mock_data/profile/jinter.json';

const localVue = createLocalVue(Vuex);

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
        cardDisplayDates: {
          comparison_date: dayjs("2013-04-15T00:00:01"),
        },
      }
    });
  });

  it('Hide card if no active med password', async () => {
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, {store, localVue});
    await new Promise(setImmediate);
    expect(wrapper.vm.expiresMed).toBe(null);
    expect(wrapper.vm.hasActiveMedPw).toBe(null);
    expect(wrapper.vm.showCard).toBe(false);
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Show card, password expired', async () => {
    mockJinterProfile.password.expires_med = '2013-04-14 10:57:06-08:00';
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise(setImmediate); 
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.hasActiveMedPw).toBe(true);
    expect(wrapper.vm.expired).toBe(true);
    expect(wrapper.vm.expiresIn3Days).toBe(true);
    expect(wrapper.vm.expiresIn30Days).toBe(true);
    expect(wrapper.vm.expiration).toBe('Mon, Apr 14');
  });

  it('Show card, password not expired', async () => {
    mockJinterProfile.password.has_active_med_pw = true;
    mockJinterProfile.password.med_pw_expired = false;
    mockJinterProfile.password.expires_med = '2013-05-14 08:00:00-08:00';
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    let wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.expired).toBe(false);
    expect(wrapper.vm.expiresIn30Days).toBe(true);
    expect(wrapper.vm.expiresIn3Days).toBe(false);

    mockJinterProfile.password.expires_med = '2013-04-12 08:00:00-08:00';
    axios.get.mockResolvedValue({ data: mockJinterProfile, status: 200 });
    wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.expiresIn3Days).toBe(truw);
    expect(wrapper.vm.expiration).toBe(
      wrapper.vm.toFriendlyDatetime(mockJinterProfile.password.expires_med));
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
