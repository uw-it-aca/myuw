import {Vue, vueConf} from './base.js';
import utils from './mixins/utils.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';
import Textbooks from './components/textbooks/textbooks.vue';

// Vuex Stores
import instSchedule from './vuex/store/schedule/instructor';
import studSchedule from './vuex/store/schedule/student';
import textbooks from './vuex/store/textbooks';

vueConf.store.registerModule('inst_schedule', instSchedule);
vueConf.store.registerModule('stud_schedule', studSchedule);
vueConf.store.registerModule('textbooks', textbooks);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: `${utils.methods.pageTitleFromTerm(window.textbookTerm)} Textbooks`,
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-textbooks', Textbooks);

new Vue({
  ...vueConf,
});
