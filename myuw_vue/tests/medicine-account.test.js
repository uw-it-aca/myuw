import dayjs from 'dayjs';
dayjs.extend(require('dayjs/plugin/timezone'))
import axios from 'axios';
import { mount } from '@vue/test-utils';
import Vuex from 'vuex';
import { createLocalVue } from './helper';
import profile from '../vuex/store/profile';
import UwCard from '../components/_templates/card.vue';
import MedicineAccountCard from '../components/accounts/medicine-account.vue';
import FormattedDate from '../components/_common/formatted-date.vue';
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
    expect(wrapper.vm.hasActiveMedPw).toBe(false);
    expect(wrapper.vm.showCard).toBeFalsy;
    expect(wrapper.findComponent(UwCard).exists()).toBe(false);
  });

  it('Show card, password expired', async () => {
    mockJinterProfile.password.last_change_med =	"2013-01-14 10:57:06-07:00";
    mockJinterProfile.password.expires_med = '2013-04-14 10:57:06-08:00';
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    const wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise(setImmediate); 
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.vm.hasActiveMedPw).toBe(true);
    expect(wrapper.vm.expired).toBe(true);
  });

  it('Show card, password not expired', async () => {
    mockJinterProfile.password.last_change_med = "2013-01-14 10:57:06-07:00";
    mockJinterProfile.password.expires_med = '2013-05-14 00:00:00-08:00';
    axios.get.mockResolvedValue({data: mockJinterProfile, status: 200});
    let wrapper = mount(MedicineAccountCard, { store, localVue });
    await new Promise(setImmediate);
    expect(wrapper.vm.showCard).toBe(true);
    expect(wrapper.findComponent(UwCard).exists()).toBe(true);
    expect(wrapper.findComponent(FormattedDate).exists()).toBe(true);
    expect(wrapper.vm.expired).toBe(false);
  });

  it('Due in 30 days', () => {
    const wrapper = mount(
      FormattedDate,
      { store, localVue,
        propsData: {
          'dueDate': '2013-05-14 00:00:00-08:00',
          'displayTextDanger': true,
          'displayTime': true }
        }
    );
    expect(wrapper.vm.displayTextDanger).toBe(true);
    expect(wrapper.vm.displayTime).toBe(true);
    expect(wrapper.vm.daysDiff).toBe(30);
    expect(wrapper.vm.dueIn30Days).toBe(true);
    expect(wrapper.vm.dueIn3Days).toBe(false);
    expect(wrapper.vm.formattedDate).toBe('Tue, May 14');
  });

  it('Due in 3 days', () => {
    const wrapper = mount(
      FormattedDate,
      { store, localVue,
        propsData: {
          'dueDate': '2013-04-17 16:00:00-08:00',
          'displayTextDanger': true,
          'displayTime': true }
        }
    );
    expect(wrapper.vm.daysDiff).toBe(3);
    expect(wrapper.vm.dueIn30Days).toBe(true);
    expect(wrapper.vm.dueIn3Days).toBe(true);
    expect(wrapper.vm.formattedDate).toBe('Thu, Apr 18, 12:00AM');
  });
});
