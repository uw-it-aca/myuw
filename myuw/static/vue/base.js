import Vue from 'vue';
import Vuex from 'vuex';
import {library} from '@fortawesome/fontawesome-svg-core';
import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText,
} from '@fortawesome/vue-fontawesome';

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
  faCaretUp,
  faSquare as fasSquare,
  faTimes,
  faPencilAlt,
  faCheck,
  faPlus,
  faCheckCircle,
  faChevronRight,
  faChevronUp,
  faInfoCircle,
} from '@fortawesome/free-solid-svg-icons';

import {
  faEdit,
  faCreditCard,
  faCalendarAlt,
  faCalendarCheck,
  faSquare,
  faCircle,
} from '@fortawesome/free-regular-svg-icons';

// bootstrap vue plugins
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
  FormCheckboxPlugin ,
  InputGroupPlugin,
  ModalPlugin,
  LayoutPlugin,
  LinkPlugin,
  NavPlugin,
  PopoverPlugin ,
  SpinnerPlugin,
  TablePlugin ,
  TabsPlugin,
  VBTogglePlugin,
  TooltipPlugin,
} from 'bootstrap-vue';

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
library.add(faInfoCircle);
library.add(faSquare);
library.add(faSquareFull);
library.add(fasSquare);
library.add(faBars);
library.add(faLocationArrow);
library.add(faCaretRight);
library.add(faCaretDown);
library.add(faCaretUp);
library.add(faTimes);
library.add(faPencilAlt);
library.add(faCheck);
library.add(faPlus);
library.add(faCheckCircle);
library.add(faCircle);
library.add(faChevronRight);
library.add(faChevronUp);

// MARK: google analytics data stream measurement_id
const gaCode = document.body.getAttribute('data-gtag');
const hashId = document.body.getAttribute('data-hashid');
const trackingEnabled = document.body.getAttribute('data-tracking-enabled');

// fontawesome 5
Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.component('font-awesome-layers', FontAwesomeLayers);
Vue.component('font-awesome-layers-text', FontAwesomeLayersText);

// bootstrap-vue components as plugins
Vue.use(AlertPlugin);
Vue.use(BadgePlugin);
Vue.use(ButtonPlugin);
Vue.use(CardPlugin);
Vue.use(CollapsePlugin);
Vue.use(FormCheckboxPlugin );
Vue.use(FormPlugin);
Vue.use(FormGroupPlugin);
Vue.use(FormInputPlugin);
Vue.use(FormSelectPlugin);
Vue.use(InputGroupPlugin);
Vue.use(LayoutPlugin);
Vue.use(LinkPlugin);
Vue.use(NavPlugin);
Vue.use(PopoverPlugin)
Vue.use(SpinnerPlugin);
Vue.use(TabsPlugin);
Vue.use(VBTogglePlugin);
Vue.use(ModalPlugin);
Vue.use(TablePlugin);
Vue.use(TooltipPlugin);

// vuex
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    user: JSON.parse(document.getElementById('user').innerHTML),
    staticUrl: JSON.parse(document.getElementById('static_url').innerHTML),
    disableActions: JSON.parse(
        document.getElementById('disable_actions').innerHTML,
    ),
    bannerMessages: JSON.parse(
      document.getElementById('banner_messages').innerHTML,
    ),
    displayOnboardMessage: JSON.parse(
      document.getElementById('display_onboard_message').innerHTML,
    ),
    displayPopUp: JSON.parse(
      document.getElementById('display_pop_up').innerHTML,
    ),
    csrfToken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
  },
  mutations: {
    addVarToState(state, {name, value}) {
      state[name] = value;
    },
  },
});

import VueMq from 'vue-mq';
import VueObserveVisibility from 'vue-observe-visibility';

// vue-mq (media queries)
Vue.use(VueMq, {
  breakpoints: {
    // breakpoints == min-widths of next size
    mobile: 768, // tablet begins 768px
    tablet: 992, // desktop begins 992px
    desktop: Infinity,
  },
});
Vue.use(VueObserveVisibility);

// import VueObserveVisibility from 'vue-observe-visibility'
// Vue.use(VueObserveVisibility)

import Logger from './plugins/logger';
import Observer from './plugins/observer';
import TrackLink from './plugins/tracklink';
import Metadata from './plugins/metadata';

Vue.use(Logger, {
  gtag: {
    config: {
      id: gaCode,
      params: {
        anonymize_ip: true,
        user_id: hashId,
      },
    },
    enabled: trackingEnabled == 'true',
  },
  // console: {
  //   print: true,
  // },
});
Vue.use(Observer);
Vue.use(TrackLink);
Vue.use(Metadata);


Vue.config.devtools = true;

// Mixins
import courses from './mixins/courses';
import utils from './mixins/utils';
Vue.mixin(courses);
Vue.mixin(utils);

const vueConf = {
  el: '#vue_root',
  created: function() {
    // MARK: construct the page title
    document.title = store.state['pageTitle'] + ' - MyUW';
    document.getElementById('vue_root').hidden = false;
  },
  store: store,
};

vueConf.store.commit('addVarToState', {
  name: 'termData',
  value: window.term_data,
});
vueConf.store.commit('addVarToState', {
  name: 'nextTerm',
  value: window.next_term,
});
vueConf.store.commit('addVarToState', {
  name: 'cardDisplayDates',
  value: JSON.parse(document.getElementById('card_display_dates').innerHTML),
});
export {Vue, vueConf};
