import axios from 'axios';
import { statusOptions, doNothing, buildWith } from './model_builder';

const customState = {
  value: {
    recentLinks: JSON.parse(document.getElementById('recent_links').innerHTML),
    popularLinks: JSON.parse(document.getElementById('popular_links').innerHTML),
    customLinks: JSON.parse(document.getElementById('custom_links').innerHTML),
    defaultLinks: JSON.parse(document.getElementById('default_links').innerHTML),
  },
  status: {
    code: 200,
    type: statusOptions[0],
  },
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
    state.value.recentLinks = response.data.recent_links;
    state.value.popularLinks = response.data.popular_links;
    state.value.customLinks = response.data.custom_links;
    state.value.defaultLinks = response.data.default_links;
  },
  setAddStatus(state, status) {
    state.addStatus = status;
  },
}

const customActions = {
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
      url: link.url,
      label: link.label,
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