import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// calendar componenets
import CalendarTabs from './components/calendar/tabs.vue';
import SidebarLinks from './components/calendar/sidebar-links.vue';

// store
import academicEvents from './vuex/store/academic_events';
import categoryLinks from './vuex/store/category_links';

vueConf.store.registerModule('academic_events', academicEvents);
vueConf.store.registerModule('category_links', categoryLinks);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Academic Calendar',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-calendar-tabs', CalendarTabs);
Vue.component('myuw-sidebar-links', SidebarLinks);

new Vue({
  ...vueConf,
});
