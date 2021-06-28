import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// components
import HuskyExpCard from './components/husky_experience/husky-exp.vue';

// stores
import hx_toolkit from './vuex/store/hx_toolkit';

vueConf.store.registerModule('hx_toolkit', hx_toolkit);

vueConf.store.commit('addVarToState', {
  name: 'page',
  value: {
    hideTitle: false,
    title: 'Husky Experience Toolkit',
  },
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-husky-exp-card', HuskyExpCard);

new Vue({
  ...vueConf,
});
