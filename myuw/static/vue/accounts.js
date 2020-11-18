import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// accounts components
import TuitionFees from './components/accounts/tuition-fees.vue';

// stores
import tuition from './vuex/store/tuition';
import notices from './vuex/store/notices';

vueConf.store.registerModule('tuition', tuition);
vueConf.store.registerModule('notices', notices);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Accounts',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-tuition-fees', TuitionFees);

new Vue({
  ...vueConf,
});
