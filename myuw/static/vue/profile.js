import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// components
import Uname from './components/profile/user-name.vue';
import StudentProfile from './components/profile/student-profile.vue';

// stores
import directory from './vuex/store/directory';
import profile from './vuex/store/profile';

vueConf.store.registerModule('directory', directory);
vueConf.store.registerModule('profile', profile);

vueConf.store.commit('addVarToState', {
  name: 'pageTitle',
  value: 'Profile',
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-uname', Uname);
Vue.component('myuw-student-profile', StudentProfile);

new Vue({
  ...vueConf,
});
