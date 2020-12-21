import {fetchBuilder, setTermAndExtractData, buildWith} from '../model_builder';
import {
  convertSectionsTimeAndDateToDateJSObj,
  generateMeetingLocationData,
} from './common';

function postProcess(response, urlExtra) {
  let data = setTermAndExtractData(response, urlExtra);

  const courseData = data[urlExtra];
  const time_schedule_published = courseData.term.time_schedule_published;
        // {"bothell": true, "seattle": true, "tacoma": true}

  let linkedPrimaryLabel = undefined;
  convertSectionsTimeAndDateToDateJSObj(courseData.sections);
  for (let i = 0; i < courseData.sections.length; i++) {
    let section = courseData.sections[i];
    section.year = courseData.year;
    section.quarter = courseData.quarter;
    section.id = (section.year + "-" +
                  section.quarter + "-" +
                  section.curriculum_abbr.replace(/ /g, '-') + "-" +
                  section.course_number + "-" +
                  section.section_id);

    section.href = (section.year + "," +
                    section.quarter + "#" +
                    section.curriculum_abbr.replace(/ /g, '-') + "-" +
                    section.course_number + "-" +
                    section.section_id);

    section.navtarget = (section.year + "," +
                         section.quarter + "," +
                         section.curriculum_abbr + "-" +
                         section.course_number + "-" +
                         section.section_id);

    section.isLinkedSecondary = false;
    if (section.is_primary_section) {
      if (section.total_linked_secondaries) {
        linkedPrimaryLabel = section.section_label;
      }
    } else {
      // secondary section
      if (linkedPrimaryLabel &&
          section.primary_section_label === linkedPrimaryLabel) {
        // this secondary section is related to
        // the last primary section
        section.isLinkedSecondary = true;
      } else {
        linkedPrimaryLabel = undefined;
      }
    }

    // check if the enrollment is of previous term
    section.is_prev_term_enrollment = false;
    if (!section.sln &&
        !time_schedule_published[section.course_campus.toLowerCase()]) {
        section.is_prev_term_enrollment = true;
        section.prev_enrollment_year = section.year - 1;
    }

    section.instructors = [];
    section.meetings.forEach((meeting, j) => {
      meeting.id = section.id + "-meeting-" + (j + 1);
      meeting.locationData = generateMeetingLocationData(meeting);

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
    if (section.final_exam) {
      section.final_exam.locationData =
        generateMeetingLocationData(section.final_exam);
    }
  }

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
