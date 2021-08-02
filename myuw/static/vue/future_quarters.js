import {Vue, vueConf} from './base.js';
import utils from './mixins/utils.js';

import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import CourseCards from './components/_common/course/student/course-cards.vue';
import VisualSchedule from './components/_common/visual_schedule/schedule.vue';
import Textbooks from './components/_common/textbooks.vue';

// stores
import textbooks from './vuex/store/textbooks';
import studSchedule from './vuex/store/schedule/student';
import visualSchedule from './vuex/store/schedule/visual';
import iasystem from './vuex/store/iasystem';

vueConf.store.registerModule('stud_schedule', studSchedule);
vueConf.store.registerModule('iasystem', iasystem);
vueConf.store.registerModule('textbooks', textbooks);
vueConf.store.registerModule('visual_schedule', visualSchedule);

vueConf.store.commit('addVarToState', {
  name: 'futureTerm',
  value: window.futureTerm,  // "year,quarter,[ab]-term"
});

vueConf.store.commit('addVarToState', {
  name: 'page',
  value: {
    hideTitle: false,
    title: `Preview ${utils.methods.pageTitleFromTerm(window.futureTerm)}`,
  },
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-course-cards', CourseCards);
Vue.component('myuw-visual-schedule', VisualSchedule);
Vue.component('myuw-textbooks', Textbooks);

new Vue({
  ...vueConf,
});
