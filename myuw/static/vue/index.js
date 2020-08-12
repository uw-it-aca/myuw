import {Vue, store, rootId} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';

import notices from './store/notices';
import hfs from './store/hfs';
import library from './store/library';

store.registerModule('notices', notices);
store.registerModule('hfs', hfs);
store.registerModule('library', library);

store.state["termData"] = window.term_data;

Vue.component('uw-boilerplate', Boilerplate);
Vue.component('uw-summaries', Summaries);
Vue.component('uw-notices', Notices);

new Vue({
  el: `#${rootId}`,
  created: function() {
    document.getElementById(rootId).hidden = false;
  },
  store: store,
});
