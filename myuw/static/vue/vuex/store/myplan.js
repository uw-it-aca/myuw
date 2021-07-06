import { fetchBuilder, extractData, buildWith } from './model_builder';
import {
  processSectionMeetings,
} from './schedule/common';

function postProcess(response, urlExtra) {
  let data = extractData(response);

  if (Array.isArray(data) && data.length === 0) {
    data = null;
  }

  // Flatten section_data
  data?.terms?.forEach((term) => {
    term.courses?.forEach((course) => {
      for (let i = 0; i < course.sections.length; i++) {
        if (!course.sections[i].section_data) {
          // unready course may not have section_data
          continue;
        }
        course.sections[i] = course.sections[i].section_data;
        const section = course.sections[i]
        section.anchor = (section.curriculum_abbr.replace(/ /g, '-') +
          '-' + section.course_number +
          '-' + section.section_id);
        section.id = `${term.year}-${term.quarter}-${section.anchor}`;
        processSectionMeetings(section);
      }
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