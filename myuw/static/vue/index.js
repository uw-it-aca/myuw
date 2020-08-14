import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';

import notices from './store/notices';
import hfs from './store/hfs';
import library from './store/library';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);

vueConf.store.state['termData'] = window.term_data;
vueConf.store.state['pageTitle'] = 'Home';

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);

new Vue({
  ...vueConf,
});
