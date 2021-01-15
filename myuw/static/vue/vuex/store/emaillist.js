import axios from 'axios';

const customActions = {
  requestCreateEmail({rootState}, data) {
    data.csrfmiddlewaretoken = rootState.csrfToken;
    return axios.post('/api/v1/emaillist/', data);
  }
};

export default {
  namespaced: true,
  state: {},
  getters: {},
  actions: customActions,
  mutations: {},
};
