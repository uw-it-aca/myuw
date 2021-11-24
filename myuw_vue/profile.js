import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// components
import Uname from './components/profile/user-name.vue';
import StudentProfile from './components/profile/student-profile.vue';
import EmployeeProfile from './components/profile/employee-profile.vue';
import ApplicantProfile from './components/profile/applicant-profile.vue';
import ProfileHelpLinks from './components/profile/help-links.vue';

// stores
import directory from './vuex/store/directory';
import profile from './vuex/store/profile';

vueConf.store.registerModule('directory', directory);
vueConf.store.registerModule('profile', profile);

vueConf.store.commit('addVarToState', {
  name: 'page',
  value: {
    hideTitle: true,
    title: 'Profile',
  },
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-uname', Uname);
Vue.component('myuw-student-profile', StudentProfile);
Vue.component('myuw-employee-profile', EmployeeProfile);
Vue.component('myuw-applicant-profile', ApplicantProfile);
Vue.component('myuw-profile-sidelinks', ProfileHelpLinks);

new Vue({
  ...vueConf,
});
