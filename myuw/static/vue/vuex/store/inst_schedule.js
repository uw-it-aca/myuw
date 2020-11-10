import dayjs from 'dayjs';

import {fetchBuilder, setTermAndExtractData, buildWith} from './model_builder';

// Helper Functions
const tryConvertDayJS = (obj, format=undefined) => {
  if (obj) {
    return dayjs(obj, format);
  }
  return obj;
};

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  const courseData = data[urlExtra];
  courseData.sections.forEach((section) => {
    section.instructors = [];
    section.meetings.forEach((meeting) => {
      meeting.start_time = tryConvertDayJS(meeting.start_time, "hh:mm");
      meeting.end_time = tryConvertDayJS(meeting.end_time, "hh:mm");
      meeting.eos_start_date = tryConvertDayJS(meeting.eos_start_date);
      meeting.eos_end_date = tryConvertDayJS(meeting.eos_end_date);

      meeting.curriculumAbbr = section.curriculum_abbr;
      meeting.courseNumber = section.course_number;
      meeting.sectionId = section.section_id;

      meeting.instructors.forEach((instructor) => {
        if (section.instructors.findIndex(
          (inst) => inst.uwregid === instructor.uwregid) === -1) {
          section.instructors.push(instructor);
        }
      });
    });
    section.instructors.sort((ia, ib) => {
      if (ia.surname < ib.surname) { return -1;}
      if (ia.surname > ib.surname) { return 1; }
      return 0;
    });
  });

  return data;
}

const customActions = {
  fetch: fetchBuilder(
    '/api/v1/instructor_schedule/',
    postProcess,
    'json'
  ),
};

export default buildWith(
  { customActions },
);
