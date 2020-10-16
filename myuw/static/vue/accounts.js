import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts',
});

Vue.component('myuw-boilerplate', Boilerplate);

new Vue({
  ...vueConf,
});
