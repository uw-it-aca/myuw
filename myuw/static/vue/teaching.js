import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// teaching componenets
import CourseTabs from './components/teaching/course/chooser_tabs.vue';

// store
import classlist from './vuex/store/classlist';
import emaillist from './vuex/store/emaillist';
import instSchedule from './vuex/store/schedule/instructor';

vueConf.store.registerModule('classlist', classlist);
vueConf.store.registerModule('emaillist', emaillist);
vueConf.store.registerModule('inst_schedule', instSchedule);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Teaching',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-course-tabs', CourseTabs);

new Vue({
  ...vueConf,
});
