import { fetchBuilder, extractData, buildWith } from './model_builder';
import {convertSectionsTimeAndDateToDateJSObj} from './schedule/common';

function postProcess(response, urlExtra) {
  let data = extractData(response);

  if (Array.isArray(data) && data.length === 0) {
    data = null;
  }

  // Flatten section_data
  data?.terms?.forEach((term) => {
    term.courses?.forEach((course) => {
      for (let i = 0; i < course.sections.length; i++) {
        course.sections[i] = course.sections[i].section_data;
  
        course.sections[i].anchor = `${course.sections[i].curriculum_abbr}-` +
          `${course.sections[i].course_number}-${course.sections[i].section_id}`;
        course.sections[i].id = `${term.year}-${term.quarter}-${course.sections[i].anchor}`;
      }
      convertSectionsTimeAndDateToDateJSObj(course.sections);
    });
  });

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