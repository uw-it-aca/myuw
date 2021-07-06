import axios from 'axios';

const customActions = {
  requestCreateEmail(
    {rootState},
    {formData = {}, onSuccess = () => {}, onError = () => {}} = {}
  ) {
    let formDataStr = `csrfmiddlewaretoken=${rootState.csrfToken}`;

    Object.entries(formData).forEach(([key, value]) => {
      formDataStr += `&${encodeURIComponent(key)}=${encodeURIComponent(value)}`;
    });

    return axios.post(
      '/api/v1/emaillist/',
      formDataStr,
      {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    ).then(onSuccess).catch(onError);
  }
};

export default {
  namespaced: true,
  state: {},
  getters: {},
  actions: customActions,
  mutations: {},
};
