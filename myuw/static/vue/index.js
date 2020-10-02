import {Vue, vueConf} from './base.js';

// Bootstrap vue plugins
import {
  AlertPlugin,
  BadgePlugin,
  ButtonPlugin,
  CardPlugin,
  CollapsePlugin,
  FormPlugin,
  FormGroupPlugin,
  FormInputPlugin,
  FormSelectPlugin,
  LayoutPlugin,
  LinkPlugin,
  NavPlugin,
  SpinnerPlugin,
  TabsPlugin,
  VBTogglePlugin,
} from 'bootstrap-vue';

// Vue componenets
import Boilerplate from './containers/boilerplate.vue';
import Summaries from './components/index/summaries.vue';
import Notices from './components/index/cards/notices.vue';
import Applicant from './components/index/cards/applicant/applicant.vue';
import Events from './components/index/cards/events/events.vue';
import Grades from './components/cards/grades.vue';
import HuskyExperience from './components/cards/husky-experience.vue';
import InterStudent from './components/index/cards/international/student.vue';

import Outage from './components/cards/outage.vue';
import Quicklinks from './components/index/cards/quicklinks/quicklinks.vue';

import ToRegister from './components/index/cards/new_student/to-register.vue';
import RegStatus from './components/index/cards/registration/status.vue';
import CriticalInfo from
  './components/index/cards/new_student/critical-info.vue';
import ThankYou from './components/index/cards/new_student/thank-you.vue';
import NewInterStudent from
  './components/index/cards/international/new-student.vue';

import VisualSchedule from './components/cards/schedule/visual-schedule.vue';
import FutureQuarterCards from './components/cards/future-quarter.vue';
import Textbooks from './components/cards/textbooks.vue'

// Stores
import notices from './vuex/store/notices';
import quicklinks from './vuex/store/quicklinks';
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import applicant from './vuex/store/applicant';
import events from './vuex/store/events';
import courses from './vuex/store/courses';
import visual_schedule from './vuex/store/visual_schedule';
import hx_toolkit from './vuex/store/hx_toolkit';
import oquarter from './vuex/store/oquarter';
import profile from './vuex/store/profile';
import myplan from './vuex/store/myplan';
import textbooks from './vuex/store/textbooks';
import schedule from './vuex/store/schedule';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);
vueConf.store.registerModule('events', events);
vueConf.store.registerModule('courses', courses);
vueConf.store.registerModule('visual_schedule', visual_schedule);
vueConf.store.registerModule('hx_toolkit', hx_toolkit);
vueConf.store.registerModule('quicklinks', quicklinks);
vueConf.store.registerModule('oquarter', oquarter);
vueConf.store.registerModule('profile', profile);
vueConf.store.registerModule('myplan', myplan);
vueConf.store.registerModule('textbooks', textbooks);
vueConf.store.registerModule('schedule', schedule);

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

// Bootstrap-Vue components as plugins
Vue.use(AlertPlugin);
Vue.use(BadgePlugin);
Vue.use(ButtonPlugin);
Vue.use(CardPlugin);
Vue.use(CollapsePlugin);
Vue.use(FormPlugin);
Vue.use(FormGroupPlugin);
Vue.use(FormInputPlugin);
Vue.use(FormSelectPlugin);
Vue.use(LayoutPlugin);
Vue.use(LinkPlugin);
Vue.use(NavPlugin);
Vue.use(SpinnerPlugin);
Vue.use(TabsPlugin);
Vue.use(VBTogglePlugin);

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);
Vue.component('myuw-ns-critical-info', CriticalInfo);
Vue.component('myuw-ns-international-student', NewInterStudent);
Vue.component('myuw-applicant', Applicant);
Vue.component('myuw-international-student', InterStudent);
Vue.component('myuw-events', Events);
Vue.component('myuw-grades', Grades);
Vue.component('myuw-visual-schedule', VisualSchedule);
Vue.component('myuw-husky-experience', HuskyExperience);
Vue.component('myuw-outage', Outage);
Vue.component('myuw-quicklinks', Quicklinks);
Vue.component('myuw-ns-thank-you', ThankYou);
Vue.component('myuw-ns-to-register', ToRegister);
Vue.component('myuw-reg-status', RegStatus);
Vue.component('myuw-future-quarter-cards', FutureQuarterCards);
Vue.component('myuw-textbooks', Textbooks);

new Vue({
  ...vueConf,
});
