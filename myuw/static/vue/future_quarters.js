import {Vue, vueConf} from './base.js';
import utils from './mixins/utils.js';

import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import AllCourses from './components/_common/course/all-courses.vue';
import VisualSchedule from './components/_common/visual_schedule/schedule.vue';
import Textbooks from './components/_common/textbooks.vue';

// stores
import textbooks from './vuex/store/textbooks';
import studSchedule from './vuex/store/stud_schedule';
import visualSchedule from './vuex/store/visual_schedule';

vueConf.store.registerModule('stud_schedule', studSchedule);
vueConf.store.registerModule('textbooks', textbooks);
vueConf.store.registerModule('visual_schedule', visualSchedule);

vueConf.store.commit('addVarToState', {
  name: 'futureTerm',
  value: window.futureTerm,
});
vueConf.store.commit('addVarToState', {
  name: 'futureTermData',
  value: window.futureTermData,
});

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: `Preview ${utils.methods.pageTitleFromTerm(window.futureTerm)}`,
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-all-courses', AllCourses);
Vue.component('myuw-visual-schedule', VisualSchedule);
Vue.component('myuw-textbooks', Textbooks);

new Vue({
  ...vueConf,
});
