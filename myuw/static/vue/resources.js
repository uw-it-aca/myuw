import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// componenets
import ResourcesPage from './components/resources/resources.vue';

// store
import resources from './vuex/store/resources';
vueConf.store.registerModule('resources', resources);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'UW Resources',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-resources-page', ResourcesPage);

new Vue({
  ...vueConf,
});
