import {Vue, vueConf} from './base.js';

import Boilerplate from './components/layouts/boilerplate.vue';

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Teaching'
});

Vue.component('myuw-boilerplate', Boilerplate);

new Vue({
  ...vueConf,
});
