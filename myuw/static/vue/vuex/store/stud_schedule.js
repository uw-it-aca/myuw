import dayjs from 'dayjs';

import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  data[urlExtra].sections.forEach((section) => {
    section.id = (data.year + "-" + data.quarter + "-" +
                  section.curriculum_abbr + "-" +
                  section.course_number + "-" + section.section_id);

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

    section.has_eos_dates = false;
    // Convert dates and times to datejs objects
    section.meetings.forEach((meeting) => {
      meeting.id = section.id + "-meeting-" + meeting.index;
      if (meeting.start_time && meeting.end_time) {
        meeting.start_time = dayjs(meeting.start_time, "hh:mm")
          .second(0)
          .millisecond(0);
        meeting.end_time = dayjs(meeting.end_time, "hh:mm")
          .second(0)
          .millisecond(0);
      }

      if (meeting.eos_start_date && meeting.eos_end_date) {
        section.has_eos_dates = true;
        meeting.eos_start_date = dayjs(meeting.eos_start_date)
          .second(0)
          .millisecond(0);
        meeting.eos_end_date = dayjs(meeting.eos_end_date)
          .second(0)
          .millisecond(0);
      }

      if (meeting.type && meeting.type !== 'NON' &&
          meeting.type !== section.section_type) {
        meeting.display_type = true;
      }
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
