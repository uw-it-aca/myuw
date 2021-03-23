import { createLocalVue as createLocalVueOriginal } from '@vue/test-utils';
import BootstrapVue from 'bootstrap-vue';
import Vuex from 'vuex';

// Global Mixins
import utils from '../mixins/utils';

// Custom Plugins
import Logger from '../plugins/logger';
import Metadata from '../plugins/metadata';
import Tracklink from '../plugins/tracklink';
import TrackCollapse from '../plugins/trackcollapse';

// helper for testing action with expected mutations
const expectAction = (
    action, payload, state, getters, expectedMutations,
) => new Promise((done) => {
  let count = 0;

  // mock commit
  const commit = (type, payload) => {
    const mutation = expectedMutations[count];

    try {
      expect(type).toEqual(mutation.type);
      expect(payload).toEqual(mutation.payload);
    } catch (error) {
      done(error);
    }

    count++;
    if (count >= expectedMutations.length) {
      done();
    }
  };

  // call the action with mocked store and arguments
  action({commit, getters, state}, payload);

  // check if no mutations should have been dispatched
  if (expectedMutations.length === 0) {
    expect(count).toEqual(0);
    done();
  }
});

const createLocalVue = (vuexModule) => {
  const localVue = createLocalVueOriginal();
  localVue.use(BootstrapVue);
  localVue.use(vuexModule);
  localVue.use(Metadata);
  localVue.use(Logger, {
    console: {},
  });
  // Mock observer plugin
  localVue.use((vue) => {
    vue.directive('out', {});
    vue.directive('out-all', {});
  });
  localVue.use(Tracklink);
  localVue.use(TrackCollapse);
  localVue.mixin(utils);

  return localVue;
};

export {
  expectAction,
  createLocalVue,
};
