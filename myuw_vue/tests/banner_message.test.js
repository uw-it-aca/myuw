import { mount } from '@vue/test-utils';
import Vuex from 'vuex';
import { createLocalVue } from './helper';
import BannerMessage from '../components/_templates/boilerplate/banner-msg.vue';

const localVue = createLocalVue(Vuex);
const messages = [
  {
    "id": 2,
    "content": "<strong>MyUW mobile app</strong> is now available! Get it at the <a href='https://apps.apple.com/us/app/myuw/id1521514519'>Apple App Store</a> and on <a href='https://play.google.com/store/apps/details?id=edu.uw.myuw_android&hl=en_US&gl=US'>Google Play</a>",
    "level_name": "Success",
  },
  {
    "id": 3,
    "content": "Users are experiencing failed logins to UW web services, including ..., due to heavy load. Trying again often fixes the issue. See <a href='https://eoutage.uw.edu' class='external-link'>eOutage website</a> for more information.",
    "level_name": "Warning",
  }];

describe('Banner Message Component', () => {
  let store;
  beforeEach(() => {
    store = new Vuex.Store({
      state: {},
    });
  });

  it('Verify methods', () => {
    const wrapper = mount(
      BannerMessage, 
      { store, localVue, propsData: { 'messages': messages } }
    );
    expect(wrapper.vm.messageAtLevel('Info').length).toBe(1);
    expect(wrapper.vm.messageAtLevel('Warning').length).toBe(1);
    expect(wrapper.vm.styleAtLevel('Info')).toBe("msg-info");
    expect(wrapper.vm.styleAtLevel('Warning')).toBe("msg-warning");
  });
});
