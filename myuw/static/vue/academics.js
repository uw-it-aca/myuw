import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import CourseCards from './components/_common/course/course-cards.vue';
import Grades from './components/_common/grades.vue';
import Outage from './components/_common/outage.vue';
import VisualSchedule from './components/_common/visual_schedule/schedule.vue';
import Textbooks from './components/_common/textbooks.vue';
import FutureQuarterCards from './components/_common/future-quarter.vue';

// academics components
import GradStatus from './components/academics/grad-status.vue';
import SidebarLinks from './components/academics/sidebar-links.vue';
// import CourseCards from './components/academics/schedule/course-cards.vue';
import GradCommittee from './components/academics/grad-committee.vue';

// stores
import grad from './vuex/store/grad';
import notices from './vuex/store/notices';
import oquarter from './vuex/store/oquarter';
import iasystem from './vuex/store/iasystem';
import textbooks from './vuex/store/textbooks';
import studSchedule from './vuex/store/stud_schedule';
import visualSchedule from './vuex/store/visual_schedule';
import categoryLinks from './vuex/store/category_links';

vueConf.store.registerModule('grad', grad);
vueConf.store.registerModule('iasystem', iasystem);
vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('oquarter', oquarter);
vueConf.store.registerModule('stud_schedule', studSchedule);
vueConf.store.registerModule('textbooks', textbooks);
vueConf.store.registerModule('visual_schedule', visualSchedule);
vueConf.store.registerModule('category_links', categoryLinks);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Academics',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-course-cards', CourseCards);
Vue.component('myuw-grades', Grades);
Vue.component('myuw-outage', Outage);
Vue.component('myuw-future-quarter-cards', FutureQuarterCards);
Vue.component('myuw-visual-schedule', VisualSchedule);
Vue.component('myuw-textbooks', Textbooks);
Vue.component('myuw-grad-status', GradStatus);
Vue.component('myuw-grad-committee', GradCommittee);
Vue.component('myuw-sidebar-links', SidebarLinks);

new Vue({
  ...vueConf,
});
