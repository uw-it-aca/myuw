import { fetchBuilder, extractData, buildWith } from './model_builder';

function postProcess(response) {
  const data = extractData(response);
  const formattedData = {};

  if (data.terms) {
    data.terms.forEach((term) => {
      formattedData[term.quarter] = term;
    });
  }

  return formattedData;
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