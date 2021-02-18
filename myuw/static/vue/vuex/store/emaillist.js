import axios from 'axios';

const customActions = {
  requestCreateEmail({rootState}, {list = [], onError = () => {}} = {}) {
    let formDataStr = '';
    formDataStr += `csrfmiddlewaretoken=${rootState.csrfToken}`;

    list.forEach((item) => {
      formDataStr += `&${encodeURIComponent(item.key)}=${encodeURIComponent(item.label)}`;
    });

    return axios.post(
      '/api/v1/emaillist/',
      formDataStr,
      {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    ).catch(onError);
  }
};

export default {
  namespaced: true,
  state: {},
  getters: {},
  actions: customActions,
  mutations: {},
};
