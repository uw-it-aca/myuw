import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  // MUWM-549 and MUWM-552
  data[urlExtra].sections.forEach((section) => {
    let canvasUrl = section.canvas_url;
    if (canvasUrl) {
      if (section.class_website_url === canvasUrl) {
        section.class_website_url = null
      }

      let matches = canvasUrl.match(/\/([0-9]+)$/);
      let canvasId = matches[1];
      let alternateUrl = `https://uw.instructure.com/courses/${canvasId}`;

      if (section.class_website_url === alternateUrl) {
        section.class_website_url = null
      }
    }
  });

  return data;
}

const customActions = {
  fetch: fetchBuilder(
    '/api/v1/schedule/',
    postProcess,
    'json'
  ),
};

export default buildWith(
  { customActions },
);