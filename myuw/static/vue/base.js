import "core-js/stable";
import "regenerator-runtime/runtime";
import Vue from 'vue'
import Vuex from 'vuex'
import { BootstrapVue } from 'bootstrap-vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

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
library.add(faEdit);
library.add(faCreditCard);
library.add(faCalendarCheck);
library.add(faBookmark);

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(BootstrapVue)

const store = new Vuex.Store({
    state: {
        user: JSON.parse(document.getElementById('user').innerHTML),
    }
})

const rootId = "vue_root"
export { Vue, store, rootId }