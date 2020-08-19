import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';
import CriticalInfo from './components/index/cards/critical-info.vue';
import InterStudent from './components/index/cards/international/student.vue';
import NewInterStudent from 
  './components/index/cards/international/new_student.vue';
import Applicant from './components/index/cards/applicant/applicant.vue';

import notices from './store/notices';
import hfs from './store/hfs';
import library from './store/library';
import applicant from './store/applicant';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);

vueConf.store.state['termData'] = window.term_data;
vueConf.store.state['pageTitle'] = 'Home';

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);
Vue.component('myuw-critical-info', CriticalInfo);
Vue.component('myuw-international-student', InterStudent);
Vue.component('myuw-new-international-student', NewInterStudent);
Vue.component('myuw-applicant', Applicant);

new Vue({
  ...vueConf,
});
