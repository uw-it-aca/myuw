import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';
import AllNotices from './components/notices/all-notices.vue';

// stores
import notices from './vuex/store/notices';

vueConf.store.registerModule('notices', notices);

vueConf.store.commit('addVarToState', {
  name: 'page',
  value: {
    hideTitle: false,
    title: 'Notices',
  },
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-all-notices', AllNotices);

new Vue({
  ...vueConf,
});
