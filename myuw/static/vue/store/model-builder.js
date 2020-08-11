import axios from 'axios';

const statusOptions = ["READY", "FETCHING", "ERROR"];

const doNothing = (response) => response;

const buildWith = (
  endpoint,
  postProcess=doNothing,
  {custom_getters={},custom_mutations={},custom_actions={}} = {}, type="json") => {
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
    ...custom_getters
  };

  const actions = {
    fetch({commit, getters}) {
      if (!getters.is_ready && !getters.is_fetching) {
        commit('setStatus', statusOptions[1]);
        axios.get(endpoint, {
          responseType: type,
          headers: {
            'Accept': 'text/html',
          }
        }).then(postProcess).then((data)=>{
          commit('setValue', data);
          commit('setStatus', statusOptions[0]);
        }).catch((response)=>{
          commit('setStatus', statusOptions[2]);
        })
      }
    },
    ...custom_actions
  };

  const mutations = {
    setValue(state, data) {
      state.value = data;
    },
    setStatus(state, status) {
      state.status = status;
    },
    ...custom_mutations
  };

  return {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }
}


export {
  statusOptions,
  doNothing,
  buildWith,
}