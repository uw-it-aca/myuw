import {Vue, vueConf} from './base.js';

// layout components
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// teaching componenets
import CourseTabs from './components/teaching/course/chooser_tabs.vue';
import TeachingResources from './components/teaching/teaching-resources.vue';

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
Vue.component('myuw-teaching-resources', TeachingResources);
Vue.component('myuw-course-tabs', CourseTabs);

new Vue({
  ...vueConf,
});
