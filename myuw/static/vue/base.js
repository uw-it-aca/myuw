import Vue from 'vue';
import Vuex from 'vuex';
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText,
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
  faCaretRight,
  faCaretDown,
  faSquare as fasSquare,
  faTimes,
  faPencilAlt,
  faCheck,
  faPlus,
  faCheckCircle,
  faChevronRight
} from '@fortawesome/free-solid-svg-icons';

import {
  faEdit,
  faCreditCard,
  faCalendarAlt,
  faCalendarCheck,
  faSquare,
  faCircle,
} from '@fortawesome/free-regular-svg-icons';

// Bootstrap vue plugins
import {
  AlertPlugin,
  BadgePlugin,
  ButtonPlugin,
  CardPlugin,
  CollapsePlugin,
  FormPlugin,
  FormGroupPlugin,
  FormInputPlugin,
  FormSelectPlugin,
  LayoutPlugin,
  LinkPlugin,
  NavPlugin,
  SpinnerPlugin,
  TabsPlugin,
  VBTogglePlugin,
  ModalPlugin,
} from 'bootstrap-vue';

// Mixins
import outlink from './mixins/outlink';
import utils from './mixins/utils';

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
library.add(fasSquare);
library.add(faBars);
library.add(faLocationArrow);
library.add(faCaretRight);
library.add(faCaretDown);
library.add(faTimes);
library.add(faPencilAlt);
library.add(faCheck);
library.add(faPlus);
library.add(faCheckCircle);
library.add(faCircle);
library.add(faChevronRight);

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

// Bootstrap-Vue components as plugins
Vue.use(AlertPlugin);
Vue.use(BadgePlugin);
Vue.use(ButtonPlugin);
Vue.use(CardPlugin);
Vue.use(CollapsePlugin);
Vue.use(FormPlugin);
Vue.use(FormGroupPlugin);
Vue.use(FormInputPlugin);
Vue.use(FormSelectPlugin);
Vue.use(LayoutPlugin);
Vue.use(LinkPlugin);
Vue.use(NavPlugin);
Vue.use(SpinnerPlugin);
Vue.use(TabsPlugin);
Vue.use(VBTogglePlugin);
Vue.use(ModalPlugin);

// vuex
Vue.use(Vuex);

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

Vue.mixin(outlink);
Vue.mixin(utils);

const vueConf = {
  el: '#vue_root',
  created: function() {
    document.title = 'MyUW: ' + store.state['pageTitle'];
    document.getElementById('vue_root').hidden = false;
  },
  store: store,
};

vueConf.store.commit('addVarToState', {
  name: 'termData',
  value: window.term_data,
});
export {Vue, vueConf};
