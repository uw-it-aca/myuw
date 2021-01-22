import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// calendar componenets
import CalendarTabs from './components/calendar/tabs.vue';

// store
import academic_events from './vuex/store/academic_events';

vueConf.store.registerModule('academic_events', academic_events);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Academic Calendar',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-calendar-tabs', CalendarTabs);

new Vue({
  ...vueConf,
});
