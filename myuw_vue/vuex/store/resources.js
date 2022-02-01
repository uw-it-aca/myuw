import axios from 'axios';
import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

const customMutations = {
  setPinned(state, {resource, pinned}) {
    resource.is_pinned = pinned;
  },
};

const customActions = {
    fetch: fetchBuilder('/api/v1/resources/', setTermAndExtractData, 'json'),
    pin: ({commit, rootState}, resource) => {
      axios.post(`/api/v1/resources/${resource.subcat_id}/pin`, '', {
        headers: {
          'X-CSRFToken': rootState.csrfToken,
        },
      }).then(() => commit('setPinned', {resource, pinned: true})).catch(() => {});
    },
    unpin: ({commit, rootState}, resource) => {
      axios.delete(`/api/v1/resources/${resource.subcat_id}/pin`, {
        headers: {
          'X-CSRFToken': rootState.csrfToken,
        },
      }).then(() => commit('setPinned', {resource, pinned: false})).catch(() => {});
    },
};

export default buildWith(
    {customMutations, customActions},
);
