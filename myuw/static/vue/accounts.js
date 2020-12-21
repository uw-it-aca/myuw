import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import UWNetID from './components/_common/uw-netid.vue';
import HRPayroll from './components/_common/hr-payroll.vue';

// accounts components
import HfsSea from './components/accounts/hfs-sea.vue';
import HuskyCard from './components/accounts/husky.vue';
import UpassCard from './components/accounts/upass.vue';

// stores
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import profile from './vuex/store/profile';
import upass from './vuex/store/upass';

vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('profile', profile);
vueConf.store.registerModule('upass', upass);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-hfs-sea', HfsSea);
Vue.component('myuw-husky', HuskyCard);
Vue.component('myuw-uwnetid', UWNetID);
Vue.component('myuw-hr-payroll', HRPayroll);
Vue.component('myuw-upass', UpassCard);

new Vue({
  ...vueConf,
});
