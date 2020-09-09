import 'core-js/stable';
import 'regenerator-runtime/runtime';
import Vue from 'vue';
import Vuex from 'vuex';
import {BootstrapVue} from 'bootstrap-vue';
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
} from '@fortawesome/vue-fontawesome';
import VueMq from 'vue-mq';

import {
  faUser,
  faEnvelope,
  faSearch,
  faSignOutAlt,
  faHome,
  faPaw,
  faBookmark,
  faExclamationTriangle,
  faGraduationCap,
  faBars,
  faLocationArrow,
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';

import {
  faEdit,
  faCreditCard,
  faCalendarAlt,
  faCalendarCheck,
  faSquare,
} from '@fortawesome/free-regular-svg-icons';

// myuw custom theming and global styles
import '../css/myuw/custom.scss';
import '../css/myuw/global.scss';

library.add(faUser);
library.add(faEnvelope);
library.add(faSearch);
library.add(faSignOutAlt);
library.add(faHome);
library.add(faPaw);
library.add(faGraduationCap);
library.add(faEdit);
library.add(faCreditCard);
library.add(faCalendarAlt);
library.add(faCalendarCheck);
library.add(faBookmark);
library.add(faExclamationTriangle);
library.add(faSquare);
library.add(faSquareFull);
library.add(faBars);
library.add(faLocationArrow);

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);

// vuex
Vue.use(Vuex);
Vue.use(BootstrapVue);

// vue-mq (media queries)
Vue.use(VueMq, {
  breakpoints: {
    // breakpoints == min-widths of next size
    mobile: 768, // tablet begins 768px
    tablet: 992, // desktop begins 992px
    desktop: Infinity,
  },
});

const store = new Vuex.Store({
  state: {
    user: JSON.parse(document.getElementById('user').innerHTML),
    staticUrl: JSON.parse(document.getElementById('static_url').innerHTML),
    disableActions: JSON.parse(
        document.getElementById('disable_actions').innerHTML,
    ),
    csrfToken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
  },
  mutations: {
    addVarToState(state, {name, value}) {
      state[name] = value;
    },
  },
});

Vue.config.devtools = true;

const vueConf = {
  el: '#vue_root',
  created: function() {
    document.title = 'MyUW: ' + store.state['pageTitle'];
    document.getElementById('vue_root').hidden = false;
  },
  store: store,
};
export {Vue, vueConf};
