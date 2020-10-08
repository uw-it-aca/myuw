import { fetchBuilder, extractData, buildWith } from './model_builder';

function postProcess(response, urlExtra) {
  let data = extractData(response);

  if (Array.isArray(data) && data.length === 0) {
    data = [];
  }

  return {[urlExtra]: data};
}

const customActions = {
  fetch: function (vuexObject, {year, quarter}) {
    return fetchBuilder(
      '/api/v1/myplan/', postProcess, 'json'
    )(vuexObject, `${year}/${quarter}`);
  },
};

export default buildWith(
  { customActions },
);