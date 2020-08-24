import {Vue, vueConf} from './base.js';

import Boilerplate from './containers/boilerplate.vue';

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts'
});

Vue.component('myuw-boilerplate', Boilerplate);

new Vue({
  ...vueConf,
});
