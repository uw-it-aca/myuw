import {fetchBuilder, setTermAndExtractData, buildWith} from '../model_builder';
import {
  convertSectionsTimeAndDateToDateJSObj,
} from './common';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  let courseData = data[urlExtra];
  convertSectionsTimeAndDateToDateJSObj(courseData.sections);
  for (let i = 0; i < courseData.sections.length; i++) {
    let section = courseData.sections[i];
    section.year = courseData.year;
    section.quarter = courseData.quarter;
    section.futureTerm = courseData.future_term;
    section.pastTerm = courseData.past_term;
    section.requestSummerTerm = courseData.summer_term;
    section.anchor = (section.curriculum_abbr.replace(/ /g, '-') + "-" +
                  section.course_number + "-" + section.section_id);
    section.id = (courseData.year + "-" + courseData.quarter + "-" +
                  section.anchor);

    // MUWM-549 and MUWM-552
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

    let seenInstRegids = new Set();
    section.instructors = [];
    // Convert dates and times to datejs objects
    for (let idx = 0; idx < section.meetings.length; idx++) {
      let meeting = section.meetings[idx];
      meeting.id = section.id + "-meeting-" + (idx + 1);

      for (let ii = 0; ii < meeting.instructors.length; ii++) {
        let inst = meeting.instructors[ii];
        if (!seenInstRegids.has(inst.uwregid)) {
          seenInstRegids.add(inst.uwregid);
          section.instructors.push(inst);
        }
      }
    }

    section.instructors = section.instructors.sort((i1, i2) => {
        if (i1.surname < i2.surname) return -1;
        if (i1.surname > i2.surname) return 1;
        return 0;
      });
  }
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
