import {fetchBuilder, setTermAndExtractData, buildWith} from '../model_builder';
import {
  processSectionDates,
  processSectionMeetings,
} from './common';

export function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  let courseData = data[urlExtra];

  courseData.sections.forEach((section) => {
    section.year = courseData.year;
    section.quarter = courseData.quarter;
    section.futureTerm = courseData.future_term;
    section.pastTerm = courseData.past_term;
    section.requestSummerTerm = courseData.summer_term;
    section.anchor = (section.course_abbr_slug + "-" +
                  section.course_number + "-" + section.section_id);
    section.id = section.year + "-" + section.quarter + "-" + section.anchor;
    section.label = section.id.replace(/-/g, ' ');
    processSectionDates(section);

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

    processSectionMeetings(section);

    let seenInstRegids = new Set();
    section.instructors = [];
    // Convert dates and times to datejs objects
    section.meetings.forEach((meeting) => {
      meeting.instructors.forEach((instructor) => {
        if (!seenInstRegids.has(instructor.uwregid)) {
          seenInstRegids.add(instructor.uwregid);
          section.instructors.push(instructor);
        }
      });
    });

    section.instructors = section.instructors.sort((i1, i2) => {
      if (i1.surname < i2.surname) return -1;
      if (i1.surname > i2.surname) return 1;
      return 0;
    });
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
