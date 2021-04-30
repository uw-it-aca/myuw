import { fetchBuilder, extractData, buildWith } from './model_builder';
import {
  tryConvertDayJS,
} from './schedule/common';

function postProcess(response, urlExtra) {
  let data = extractData(response);

  if (Array.isArray(data) && data.length === 0) {
    data = null;
  }

  if (data.term.length && data.term[0].courses) {
    data.term[0].courses.forEach((course) => {
      course.sections.forEach((section) => {
        section.section_data.meetings.forEach((meeting) => {
          meeting.start_time = tryConvertDayJS(meeting.start_time, "hh:mm");
          meeting.end_time = tryConvertDayJS(meeting.end_time, "hh:mm");
        });
      });
    });
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