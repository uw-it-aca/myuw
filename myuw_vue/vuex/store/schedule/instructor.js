import axios from 'axios';
import {
  fetchBuilder,
  tryForceFetchBuilder,
  setTermAndExtractData,
  buildWith
} from '../model_builder';
import {
  processSectionDates,
  processSectionMeetings,
} from './common';
import {
  dayjs,
  getNow,
} from '../common';

const fmt = 'MMM D [at] h:mm A z';

function postProcess(response, urlExtra, rootState) {
  let data = setTermAndExtractData(response, urlExtra);

  const courseData = data[urlExtra];
  courseData.now = getNow(rootState);

  let linkedPrimaryLabel = undefined;
  courseData.sections.forEach((section) => {
    section.year = courseData.year;
    section.quarter = courseData.quarter;
    section.futureTerm = courseData.future_term;
    section.pastTerm = courseData.past_term;
    section.requestSummerTerm = courseData.summer_term;
    section.registrationStart = courseData.term.registration_periods[0].start;
    section.timeSchedulePublished = courseData.term.time_schedule_published;
    section.anchor = (section.course_abbr_slug + "-" +
                  section.course_number + "-" + section.section_id);
    section.id = section.year + "-" + section.quarter + "-" + section.anchor;
    section.label = section.id.replace(/-/g, ' ');
    processSectionDates(section);

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

    processSectionMeetings(section);

    section.instructors = [];
    section.meetings.forEach((meeting) => {
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

  addCourseGradeData(courseData);
  addCourseEvalData(courseData);

  return data;
}

function addSectionGradeData(data, section, now, near_date_threshold) {
  // MUWM-4795
  data.open = dayjs(section.grading_open_date);
  data.isOpen = section.grading_period_is_open;
  data.isClosed = section.grading_period_is_past;
  data.openRelative = data.open.from(now);
  data.deadlineRelative = data.deadline.from(now);

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
  return data;
}

function addCourseGradeData(courseData) {
  const now = courseData.now;
  const near_date_threshold = 5;
  courseData.sections.forEach((section) => {
    const courseCampus = section.course_campus.toLowerCase();
    section.isSeattle = courseCampus === 'seattle';
    section.isBothell = courseCampus === 'bothell';
    section.isTacoma = courseCampus === 'tacoma';
    
    section.isPrevTermEnrollment = (section.sln === 0 &&
      courseCampus in section.timeSchedulePublished &&
      !section.timeSchedulePublished[courseCampus]);

    // Copy over all the fields we generated in data
    section['gradingPeriod'] = addSectionGradeData(
      { deadline: dayjs(courseData.term.grade_submission_deadline),},
      section, now, near_date_threshold);

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
    } else {
      section.grading_status = {};
    }

    section.gradeSubmissionSectionDelegate =
      section.grade_submission_delegates.some((delegate) => delegate.level === 'section');
  });
}

function addCourseEvalData(courseData) {
  courseData.sections.forEach((section) => {
    if (section.evaluation) {
      section.evaluation.responseRatePercent = 0;
      if (section.evaluation.response_rate) {
        section.evaluation.responseRatePercent = Math.round(section.evaluation.response_rate * 100);
      }
      if (section.evaluation.eval_open_date) {
        let evalOpen = dayjs(section.evaluation.eval_open_date);
        section.evaluation.evalOpenDateDisplay = evalOpen.format(fmt);
      }
      if (section.evaluation.eval_close_date) {
        let evalClose = dayjs(section.evaluation.eval_close_date);
        section.evaluation.evalCloseDateDisplay = evalClose.format(fmt);
      }
      if (section.evaluation.report_available_date) {
        var reportDate = dayjs(section.evaluation.report_available_date);
        section.evaluation.reportAvailableDateDisplay = reportDate.format(fmt);
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
  toggleMini: ({ commit }, section) => {
    const toggleEndpoint = section.mini_card
      ? `/api/v1/inst_section_display/${section.apiTag}/close_mini`
      : `/api/v1/inst_section_display/${section.apiTag}/pin_mini`;
    // console.trace();
    return axios.get(toggleEndpoint)
      .then((resp) => {
        commit('updateMiniPinned', { section, pin: !section.mini_card });
      })
      .catch((error) => {
        console.error('Error toggling mini card:', error);
      });
  },
};

export default buildWith(
  { customMutations, customActions },
);
