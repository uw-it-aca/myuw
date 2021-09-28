import { createLocalVue } from '@vue/test-utils';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import VueObserveVisibility from 'vue-observe-visibility';

// Global Mixins
import utils from '../../myuw/static/vue/mixins/utils';

// Custom Plugins
import Logger from '../../myuw/static/vue/plugins/logger';
import Observer from '../../myuw/static/vue/plugins/observer';
import Metadata from '../../myuw/static/vue/plugins/metadata';
import Tracklink from '../../myuw/static/vue/plugins/tracklink';
import UwBootstrap from '../../myuw/static/vue/plugins/uw-bootstrap';

Cypress.Commands.add('createLocalVue', (vuex) => {
  let localVue = createLocalVue();
  localVue.use(vuex);

  localVue.component('font-awesome-icon', FontAwesomeIcon);
  localVue.use(Metadata);
  localVue.use(Logger, {
    console: {},
  });
  localVue.use(Observer);
  localVue.use(VueObserveVisibility);
  localVue.use(UwBootstrap);
  // Mock directive
  localVue.use((vue) => {
    vue.directive('out', {});
    vue.directive('no-track-collapse', {});
    vue.directive('visibility-change', {});
  });
  // Mock $mq
  localVue.mixin({
    created() {
      this.$mq = 'desktop';
    },
  });
  localVue.use(Tracklink);
  // localVue.use(TrackCollapse);
  localVue.mixin(utils);

  return localVue;
});

Cypress.Commands.add('componentWaitUntil', (condition) => {
  cy.wrap({componentWaitUntil: () => condition(Cypress?.vueWrapper?.vm ?? {})}, {log: false})
    .invoke('componentWaitUntil')
    .should('eq', true);
});

Cypress.Commands.add('invm', (value) => {
  return cy.wrap({invm: () => value(Cypress?.vueWrapper?.vm ?? {})}, {log: false})
    .invoke('invm');
});