import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';
import InterStudent from './components/index/cards/international/student.vue';
import NewInterStudent from 
  './components/index/cards/international/new_student.vue';
import Applicant from './components/index/cards/applicant/applicant.vue';
import Events from './components/index/cards/events/events.vue';

import notices from './store/notices';
import hfs from './store/hfs';
import library from './store/library';
import applicant from './store/applicant';
import events from './store/events';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);
vueConf.store.registerModule('events', events);

vueConf.store.commit('addVarToState', {
  name: 'termData',
  value: window.term_data
});
vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Home'
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);
Vue.component('myuw-international-student', InterStudent);
Vue.component('myuw-new-international-student', NewInterStudent);
Vue.component('myuw-applicant', Applicant);
Vue.component('myuw-events', Events);

new Vue({
  ...vueConf,
});
