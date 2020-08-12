import {Vue, store, rootId} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Notices from './components/index/cards/notices.vue';

Vue.component('uw-boilerplate', Boilerplate);
Vue.component('uw-notices', Notices);

new Vue({
  el: `#${rootId}`,
  created: function() {
    document.getElementById(rootId).hidden = false;
  },
  store: store,
});
