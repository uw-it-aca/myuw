import axios from 'axios';
import dayjs from 'dayjs';
import {
  fetchBuilder,
  tryForceFetchBuilder,
  setTermAndExtractData,
  buildWith
} from '../model_builder';
import {
  convertSectionsTimeAndDateToDateJSObj,
  generateMeetingLocationData,
} from './common';

dayjs.extend(require('dayjs/plugin/advancedFormat'))
dayjs.extend(require('dayjs/plugin/calendar'))
dayjs.extend(require('dayjs/plugin/relativeTime'))
dayjs.extend(require('dayjs/plugin/timezone'))

const fmt = 'MMM D [at] h:mm A z';

function postProcess(response, urlExtra, rootState) {
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
    section.pastTerm = courseData.past_term;
    section.anchor = (section.course_abbr_slug + "-" +
                  section.course_number + "-" + section.section_id);
    section.id = section.year + "-" + section.quarter + "-" + section.anchor;

    section.apiTag = `${section.year},${section.quarter.toLowerCase()},${
      section.curriculum_abbr
    },${section.course_number}/${section.section_id}`;

    section.href = section.year + "," + section.quarter + "#" + section.anchor;

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

  addCourseGradeData(courseData);
  addCourseEvalData(courseData, rootState);

  return data;
}

function addCourseGradeData(courseData) {
  let now = dayjs();
  let data = {
    isOpen: courseData.grading_period_is_open,
    isClosed: courseData.grading_period_is_past,
    open: dayjs(courseData.term.grading_period_open),
    deadline: dayjs(courseData.term.grade_submission_deadline),
  };

  data.openRelative = data.open.from(now);
  data.deadlineRelative = data.deadline.from(now);

  const near_date_threshold = 5;

  if (Math.abs(data.open.diff(now, 'days')) > near_date_threshold) {
    data.openFmt = data.open.format(fmt);
  } else {
    data.openFmt = data.open.calendar(now);
  }

  if (Math.abs(data.deadline.diff(now, 'days')) > near_date_threshold) {
    data.deadlineFmt = data.deadline.format(fmt);
  } else {
    data.deadlineFmt = data.deadline.calendar(now);
  }

  data.opensIn24Hours = !data.open.diff(now, 'days');
  data.deadlineIn24Hours = !data.deadline.diff(now, 'days');

  courseData.sections.forEach((section) => {
    const courseCampus = section.course_campus.toLowerCase();
    section.isSeattle = courseCampus === 'seattle';
    section.isBothell = courseCampus === 'bothell';
    section.isTacoma = courseCampus === 'tacoma';

    section.year = courseData.year;
    section.quarter = courseData.quarter;
    section.futureTerm = courseData.future_term;
    section.pastTerm = courseData.past_term;
    section.requestSummerTerm = courseData.summer_term;

    section.registrationStart = courseData.term.registration_periods[0].start;
    section.timeSchedulePublished = courseData.term.time_schedule_published;

    let allPublished = true;
    for (let campus in section.timeSchedulePublished) {
      allPublished = allPublished && section.timeSchedulePublished[campus];
      if (!allPublished) { break; }
    }

    const notPublishedOnCourseCampus = courseCampus in section.timeSchedulePublished &&
      !section.timeSchedulePublished[courseCampus];
    
    section.isPrevTermEnrollment = false;
    if (!allPublished && section.sln === 0 && notPublishedOnCourseCampus) {
      section.isPrevTermEnrollment = true;
      section.prevEnrollmentYear = this.year - 1;
    }

    // Copy over all the fields we generated in data
    section['gradingPeriod'] = data;

    if ('grading_status' in section && section.grading_status) {
      section.grading_status.allGradesSubmitted =
        section.grading_status.unsubmitted_count === 0;

      if (
        section.grading_status.submitted_date &&
        section.grading_status.submitted_date !== 'None'
      ) {
        let submitted = dayjs(section.grading_status.submitted_date);
        if (Math.abs(submitted.diff(now, 'days')) > near_date_threshold) {
          section.grading_status.submittedFmt = submitted.format(fmt);
        } else {
          section.grading_status.submittedFmt = submitted.calendar(now);
        }
      }
    }

    section.gradeSubmissionSectionDelegate =
      section.grade_submission_delegates.some((delegate) => delegate.level === 'section');
  });
}

function addCourseEvalData(courseData, rootState) {
  let comparisonDate = null;
  if (rootState &&
      rootState.cardDisplayDates &&
      rootState.cardDisplayDates.comparison_date) {
    comparisonDate = dayjs(rootState.cardDisplayDates.comparison_date);
  } else {
    comparisonDate = dayjs();
  }
  
  courseData.sections.forEach((section) => {
    if (section.evaluation) {
      section.evaluation.responseRatePercent = 0;
      section.evaluation.isPast = false;
      if (section.evaluation.response_rate) {
        section.evaluation.responseRatePercent = Math.round(section.evaluation.response_rate * 100);
      }
      if (section.evaluation.eval_open_date) {
        let evalOpen = dayjs(section.evaluation.eval_open_date);
        section.evaluation.evalOpenDateDisplay = evalOpen.format(fmt);
        section.evaluation.isOpen = comparisonDate.isAfter(evalOpen);
      }
      if (section.evaluation.eval_close_date) {
        let evalClose = dayjs(section.evaluation.eval_close_date);
        section.evaluation.evalCloseDateDisplay = evalClose.format(fmt);
        section.evaluation.inPast = comparisonDate.isAfter(evalClose);
        if (section.evaluation.isPast) {
          section.evaluation.is_open = false;
        }
      }
      if (section.evaluation.report_available_date) {
        var reportDate = dayjs(section.evaluation.report_available_date);
        section.evaluation.reportAvailableDateDisplay = reportDate.format(fmt);
        section.evaluation.reportIsAvailable = comparisonDate.isAfter(reportDate);
      }
    }
  });
}

const customMutations = {
  updateMiniPinned: (state, {section, pin}) => {
    for (let term in state.value) {
      state.value[term].sections.filter(
        (s) => s.section_label === section.section_label
      ).forEach((section) => section.mini_card = pin);
    }
  }
}

const customActions = {
  fetch: fetchBuilder(
    '/api/v1/instructor_schedule/',
    postProcess,
    'json'
  ),
  tryForceFetch: tryForceFetchBuilder(
    '/api/v1/instructor_schedule/',
    postProcess,
    'json'
  ),
  toggleMini: ({commit}, section) => {
    if (section.mini_card) {
      axios.get(`api/v1/inst_section_display/${section.apiTag}/close_mini`)
        .then((resp) => {
          commit('updateMiniPinned', {section, pin: false});
        });
    } else {
      axios.get(`api/v1/inst_section_display/${section.apiTag}/pin_mini`)
        .then((resp) => {
          commit('updateMiniPinned', {section, pin: true});
        });
    }
  },
};

export default buildWith(
  { customMutations, customActions },
);
