import axios from 'axios';
import {
  statusOptions,
  extractData,
  fetchBuilder,
  buildWith
} from './model_builder';

const customState = {
  value: [],
  status: {},
  addStatus: {
    code: 200,
    type: statusOptions[0],
  }
}

const customGetters = {
  isAddReady(state) {
    return state.addStatus !== null && state.addStatus.type == statusOptions[0];
  },
  isAddFetching(state) {
    return state.addStatus !== null && state.addStatus.type == statusOptions[1];
  },
  isAddErrored(state) {
    return state.addStatus !== null && state.addStatus.type == statusOptions[2];
  },
  addStatusCode(state) {
    return state.addStatus === null ? -1 : state.addStatus.code;
  },
};

const customMutations = {
  updateFromResponse(state, response) {
    state.value = extractData(response);
  },
  setAddStatus(state, status) {
    state.addStatus = status;
  },
}

const customActions = {
  fetch: fetchBuilder('/api/v1/link/', extractData, 'json'),
  addLink({commit, rootState}, link) {
    commit('setAddStatus', {type: statusOptions[1]});
    axios.post('/api/v1/link', {
      type: link.type || "custom",
      ...link,
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    }).then((response) => {
      commit('updateFromResponse', response);
      commit('setAddStatus', {type: statusOptions[0], code: response.statusCode});
    }).catch((e) => {
      console.log(e);
      commit('setAddStatus', {type: statusOptions[2], code: e.statusCode});
    });
  },
  removeLink({commit, rootState}, {link, canActuallyRemove}) {
    axios.post('/api/v1/link', {
      type: canActuallyRemove ? 'remove' : 'hide',
      id: canActuallyRemove ? `${link.id}` : link.url,
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    }).then((response) => commit('updateFromResponse', response)).catch(console.log);
  },
  updateLink({commit, rootState}, link) {
    axios.post('/api/v1/link', {
      type: "custom-edit",
      url: link.url.trim(),
      label: link.label.trim(),
      id: `${link.id}`,
    }, {
      headers: {
        'X-CSRFToken': rootState.csrfToken,
      },
    }).then((response) => commit('updateFromResponse', response)).catch(() => {});
  }
}

export default buildWith(
  { customState, customGetters, customMutations, customActions },
);