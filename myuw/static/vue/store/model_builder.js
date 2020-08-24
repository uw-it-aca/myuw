import axios from 'axios';

const statusOptions = ['READY', 'FETCHING', 'ERROR'];

// Some helper functions
const doNothing = (response) => response;
const extractData = (response) => response.data;

const buildWith = (
    endpoint,
    postProcess,
    {
      customGetters={},
      customMutations={},
      customActions={},
    } = {}, type='json') => {
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

  const actions = {
    fetch({commit, getters}) {
      if (!getters.isReady && !getters.isFetching) {
        commit('setStatus', statusOptions[1]);
        axios.get(endpoint, {
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
    },
    ...customActions,
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
    actions,
    mutations,
  };
};


export {
  statusOptions,
  doNothing,
  extractData,
  buildWith,
};
