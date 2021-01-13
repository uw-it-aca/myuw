import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import UWNetID from './components/_common/uw-netid.vue';
import HRPayroll from './components/_common/hr-payroll.vue';

// accounts components
import HfsSea from './components/accounts/hfs-sea.vue';
import HuskyCard from './components/accounts/husky.vue';
import MedicineAccount from './components/accounts/medicine-account.vue';
import UpassCard from './components/accounts/upass.vue';
import LibraryCard from './components/accounts/library.vue';
import TuitionFees from './components/accounts/tuition-fees.vue';

// stores
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import profile from './vuex/store/profile';
import upass from './vuex/store/upass';
import tuition from './vuex/store/tuition';
import notices from './vuex/store/notices';

vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('profile', profile);
vueConf.store.registerModule('upass', upass);
vueConf.store.registerModule('tuition', tuition);
vueConf.store.registerModule('notices', notices);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-hfs-sea', HfsSea);
Vue.component('myuw-husky', HuskyCard);
Vue.component('myuw-uwnetid', UWNetID);
Vue.component('myuw-hr-payroll', HRPayroll);
Vue.component('myuw-medicine-account', MedicineAccount);
Vue.component('myuw-upass', UpassCard);
Vue.component('myuw-library', LibraryCard);
Vue.component('myuw-tuition-fees', TuitionFees);

new Vue({
  ...vueConf,
});
