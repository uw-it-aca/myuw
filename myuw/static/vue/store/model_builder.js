import axios from 'axios';

const statusOptions = ['READY', 'FETCHING', 'ERROR'];

// Some helper functions
const doNothing = (response) => response;
const extractData = (response) => response.data;

const fetchBuilder = (url, postProcess, type) => {
  return ({commit, getters}, urlExtra = '') => {
    if (!getters.isReady && !getters.isFetching) {
      commit('setStatus', {type: statusOptions[1]});
      axios.get(url + urlExtra, {
        responseType: type,
        headers: {
          'Accept': 'text/html',
        },
      }).then((response) => {
        return {
          data: postProcess(response, urlExtra),
          statusCode: response.status
        };
      }).then(({data, statusCode}) => {
        commit('setValue', data);
        commit('setStatus', {type: statusOptions[0], code: statusCode});
      }).catch((error)=>{
        if (process.env.NODE_ENV === "development") {
          console.log(error);
        };
        commit('setStatus', {
          type: statusOptions[2], code: error.response.status
        });
      });
    }
  };
};

const buildWith = (
    {
      customState={
        value: null,
        status: null,
      },
      customGetters={},
      customMutations={},
      customActions={},
    } = {}) => {
  const state = () => customState;

  const getters = {
    isReady(state) {
      return state.status !== null && state.status.type == statusOptions[0];
    },
    isFetching(state) {
      return state.status !== null && state.status.type == statusOptions[1];
    },
    isErrored(state) {
      return state.status !== null && state.status.type == statusOptions[2];
    },
    statusCode(state) {
      return state.status === null ? -1 : state.status.code;
    },
    ...customGetters,
  };

  const mutations = {
    setValue(state, data) {
      state.value = data;
    },
    setStatus(state, status) {
      state.status = status;
    },
    ...customMutations,
  };

  return {
    namespaced: true,
    state,
    getters,
    actions: customActions,
    mutations,
  };
};


export {
  statusOptions,
  doNothing,
  extractData,
  buildWith,
  fetchBuilder,
};
