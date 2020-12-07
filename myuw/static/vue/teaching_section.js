import {Vue, vueConf} from './base.js';
import utils from './mixins/utils.js';

import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';
import Classlist from './components/classlist/class-student-list.vue';

// stores
import classlist from './vuex/store/classlist';

vueConf.store.registerModule('classlist', classlist);

vueConf.store.commit('addVarToState', {
  name: 'sectionLabel',
  value: window.section,  // "year,quarter,abbr,num/id"
});

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: `Classlist ${window.section}`,
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-classlist', Classlist);

new Vue({
  ...vueConf,
});
