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
import CriticalInfo from './components/index/cards/new_student/critical-info.vue';
import InterStudent from './components/index/cards/international/student.vue';
import NewInterStudent from
  './components/index/cards/international/new-student.vue';
import Applicant from './components/index/cards/applicant/applicant.vue';
import Events from './components/index/cards/events/events.vue';
import Grades from './components/cards/grades.vue';
import VisualSchedule from './components/cards/schedule/visual-schedule.vue';
import HuskyExperience from './components/cards/husky-experience.vue'
import Outage from './components/cards/outage.vue'
import Quicklinks from './components/index/cards/quicklinks/quicklinks.vue'
import RegStatus from './components/index/cards/reg_status/status.vue';

// Stores
import notices from './store/notices';
import quicklinks from './store/quicklinks';
import hfs from './store/hfs';
import library from './store/library';
import applicant from './store/applicant';
import events from './store/events';
import courses from './store/courses';
import schedule from './store/schedule';
import hx_toolkit from './store/hx_toolkit';
import oquarter from './store/oquarter';
import profile from './store/profile';
import myplan from './store/myplan';

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
Vue.component('myuw-reg-status', RegStatus);

new Vue({
  ...vueConf,
});
