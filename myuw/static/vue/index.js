import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';
import CriticalInfo from './components/index/cards/new_student/critical-info.vue';
import InterStudent from './components/index/cards/international/student.vue';
import NewInterStudent from 
  './components/index/cards/international/new_student.vue';
import Applicant from './components/index/cards/applicant/applicant.vue';
import Events from './components/index/cards/events/events.vue';
import Grades from './components/cards/grades.vue';

import notices from './store/notices';
import hfs from './store/hfs';
import library from './store/library';
import applicant from './store/applicant';
import events from './store/events';
import courses from './store/courses';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);
vueConf.store.registerModule('events', events);
vueConf.store.registerModule('courses', courses);

vueConf.store.commit('addVarToState', {
  name: 'termData',
  value: window.term_data
});
vueConf.store.commit('addVarToState', {
  name: 'cardDisplayDates',
  value: JSON.parse(document.getElementById('card_display_dates').innerHTML),
});
vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Home'
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);
Vue.component('myuw-ns-critical-info', CriticalInfo);
Vue.component('myuw-ns-international-student', NewInterStudent);
Vue.component('myuw-applicant', Applicant);
Vue.component('myuw-international-student', InterStudent);
Vue.component('myuw-events', Events);
Vue.component('myuw-grades', Grades);

new Vue({
  ...vueConf,
});
