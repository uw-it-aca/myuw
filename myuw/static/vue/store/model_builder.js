import axios from 'axios';

const statusOptions = ['READY', 'FETCHING', 'ERROR'];

// Some helper functions
const doNothing = (response) => response;
const extractData = (response) => response.data;

const fetchBuilder = (url, postProcess, type) => {
  return ({commit, getters}, urlExtra = '') => {
    if (!getters.isReady && !getters.isFetching) {
      commit('setStatus', statusOptions[1]);
      axios.get(url + urlExtra, {
        responseType: type,
        headers: {
          'Accept': 'text/html',
        },
      }).then(postProcess).then((data)=>{
        commit('setValue', data);
        commit('setStatus', statusOptions[0]);
      }).catch((error)=>{
        if (process.env.NODE_ENV === "development") {
          console.log(error);
        };
        commit('setStatus', statusOptions[2]);
      });
    }
  };
};

const buildWith = (
    {
      customGetters={},
      customMutations={},
      customActions={},
    } = {}) => {
  const state = () => ({
    value: [],
    status: null,
  });

  const getters = {
    isReady(state) {
      return state.status == statusOptions[0];
    },
    isFetching(state) {
      return state.status == statusOptions[1];
    },
    isErrored(state) {
      return state.status == statusOptions[2];
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
