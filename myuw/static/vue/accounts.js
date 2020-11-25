import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import UWNetID from './components/_common/uw-netid.vue';

// accounts components
import HfsSea from './components/accounts/hfs-sea.vue';

// stores
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import profile from './vuex/store/profile';

vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('profile', profile);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-hfs-sea', HfsSea);
Vue.component('myuw-uwnetid', UWNetID);

new Vue({
  ...vueConf,
});
