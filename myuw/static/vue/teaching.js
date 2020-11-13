import {Vue, vueConf} from './base.js';

// layout components
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// teaching components
import TeachingResources from './components/teaching/teaching-resources.vue';

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Teaching',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-teaching-resources', TeachingResources);

new Vue({
  ...vueConf,
});
