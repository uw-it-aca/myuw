import { Vue, vueConf } from './base.js';

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

// layout componenets
import Boilerplate from './components/layouts/boilerplate.vue';

// shared components
import Grades from './components/shared/cards/grades.vue';
import HuskyExperience from './components/shared/cards/husky-experience.vue';
import Outage from './components/shared/cards/outage.vue';
import FutureQuarterCards from './components/shared/cards/future-quarter.vue';
import VisualSchedule from './components/shared/cards/schedule/visual-schedule.vue';

// home components
import Summaries from './components/pages/home/summaries.vue';
import Notices from './components/pages/home/cards/notices.vue';
import Applicant from './components/pages/home/cards/applicant/applicant.vue';
import Events from './components/pages/home/cards/events/events.vue';
import InterStudent from './components/pages/home/cards/international/student.vue';
import Quicklinks from './components/pages/home/cards/quicklinks/quicklinks.vue';
import ToRegister from './components/pages/home/cards/new_student/to-register.vue';
import RegStatus from './components/pages/home/cards/registration/status.vue';
import CriticalInfo from './components/pages/home/cards/new_student/critical-info.vue';
import ThankYou from './components/pages/home/cards/new_student/thank-you.vue';
import NewInterStudent from './components/pages/home/cards/international/new-student.vue';
import UWNetID from './components/pages/home/cards/accounts/uwnetid.vue';

// Stores
import notices from './vuex/store/notices';
import quicklinks from './vuex/store/quicklinks';
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import applicant from './vuex/store/applicant';
import events from './vuex/store/events';
import courses from './vuex/store/courses';
import schedule from './vuex/store/schedule';
import hx_toolkit from './vuex/store/hx_toolkit';
import oquarter from './vuex/store/oquarter';
import profile from './vuex/store/profile';
import myplan from './vuex/store/myplan';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);
vueConf.store.registerModule('events', events);
vueConf.store.registerModule('courses', courses);
vueConf.store.registerModule('schedule', schedule);
vueConf.store.registerModule('hx_toolkit', hx_toolkit);
vueConf.store.registerModule('quicklinks', quicklinks);
vueConf.store.registerModule('oquarter', oquarter);
vueConf.store.registerModule('profile', profile);
vueConf.store.registerModule('myplan', myplan);

vueConf.store.commit('addVarToState', {
  name: 'termData',
  value: window.term_data,
});
vueConf.store.commit('addVarToState', {
  name: 'cardDisplayDates',
  value: JSON.parse(document.getElementById('card_display_dates').innerHTML),
});
vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Home',
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
Vue.component('myuw-uwnetid', UWNetID);

new Vue({
  ...vueConf,
});
