import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// teaching componenets
import CourseTabs from './components/teaching/course/tabs.vue';

// store
import instSchedule from './vuex/store/inst_schedule';

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
