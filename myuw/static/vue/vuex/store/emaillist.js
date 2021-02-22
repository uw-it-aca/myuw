import axios from 'axios';

const customActions = {
  requestCreateEmail(
    {rootState},
    {list = [], onSuccess = () => {}, onError = () => {}} = {}
  ) {
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
    ).then(onSuccess).catch(onSuccess);
  }
};

export default {
  namespaced: true,
  state: {},
  getters: {},
  actions: customActions,
  mutations: {},
};
