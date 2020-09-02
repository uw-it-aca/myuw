import { fetchBuilder, extractData, buildWith } from './model_builder';

const customActions = {
  fetch: function (vuexObject, year, quarter) {
    return fetchBuilder(
      '/api/v1/profile/', extractData, 'json'
    )(vuexObject, `${year}/${quarter}`);
  },
};

export default buildWith(
  { customActions },
);