import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// components


// stores
import profile from './vuex/store/profile';

vueConf.store.registerModule('profile', profile);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Profile',
});

Vue.component('myuw-boilerplate', Boilerplate);

new Vue({
  ...vueConf,
});
