import "core-js/stable";
import "regenerator-runtime/runtime";
import Vue from 'vue'
import Vuex from 'vuex'
import { BootstrapVue } from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import VueMq from 'vue-mq';

import {
  faUser,
  faEnvelope,
  faSearch,
  faSignOutAlt,
  faHome,
  faPaw,
  faBookmark,
  faCalendarCheck,
  faEdit,
  faCreditCard,
  faExclamationTriangle,
  faGraduationCap,
} from '@fortawesome/free-solid-svg-icons';

import {} from '@fortawesome/free-regular-svg-icons';

import '../css/bootstrap-theming.scss'
import 'bootstrap-vue/dist/bootstrap-vue.css'

library.add(faUser);
library.add(faEnvelope);
library.add(faSearch);
library.add(faSignOutAlt);
library.add(faHome);
library.add(faPaw);
library.add(faGraduationCap);
library.add(faEdit);
library.add(faCreditCard);
library.add(faCalendarCheck);
library.add(faBookmark);
library.add(faExclamationTriangle);

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(BootstrapVue)

// vue-mq (media queries)
Vue.use(VueMq, {
  breakpoints: {
    // breakpoints == min-widths of next size
    mobile: 768, // tablet begins 768px
    tablet: 992, // desktop begins 992px
    desktop: Infinity,
  }
});

const store = new Vuex.Store({
    state: {
        user: JSON.parse(document.getElementById('user').innerHTML),
        staticUrl: JSON.parse(document.getElementById('static_url').innerHTML),
    }
})

const rootId = "vue_root"
export { Vue, store, rootId }