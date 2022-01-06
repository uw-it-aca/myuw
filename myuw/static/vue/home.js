import {Vue, vueConf} from './base.js';

// layout componenets
import Boilerplate from './components/_templates/boilerplate/boilerplate.vue';

// common components
import Grades from './components/_common/grades.vue';
import HuskyExperience from './components/_common/husky-experience.vue';
import Outage from './components/_common/outage.vue';
import FutureQuarterCards from './components/_common/future-quarter.vue';
import VisualSchedule from './components/_common/visual_schedule/schedule.vue';
import Textbooks from './components/_common/textbooks.vue';
import UWNetID from './components/_common/uw-netid.vue';
import HRPayroll from './components/_common/hr-payroll.vue';

// home components
import Summaries from './components/home/summaries.vue';
import Notices from './components/home/notice/notices.vue';
import Applicant from './components/home/applicant/applicant.vue';
import Events from './components/home/events/events.vue';
import InterStudent from './components/home/international/student.vue';
import InstructorCourseSummery from
  './components/home/inst_course_summary/summary.vue';
import NewInterStudent from './components/home/international/new-student.vue';
import Quicklinks from './components/home/quicklinks/quicklinks.vue';
import ToRegister from './components/home/new_student/to-register.vue';
import ThankYou from './components/home/new_student/thank-you.vue';
import SummerEfs from './components/home/new_student/summer-efs.vue';
import CriticalInfo from './components/home/new_student/critical-info.vue';
import RegStatus from './components/home/registration/status.vue';
import Transcripts from './components/home/former_student/transcripts.vue';
import ContinuingEducation from './components/home/former_student/continuing-education.vue';
import Alumni from './components/home/alumni.vue';
import Retiree from './components/home/former_employee/retiree.vue';
import AcadCalSnippet from './components/home/calendar/acad-cal-snippet.vue';
import PinnedResourceCards from './components/home/resources/pinned-resource-cards.vue';
import ResourceExplore from './components/home/resources/resource-explore.vue';
import GraduationPreApplication from './components/home/graduation/pre-application.vue';

// stores
import notices from './vuex/store/notices';
import quicklinks from './vuex/store/quicklinks';
import hfs from './vuex/store/hfs';
import library from './vuex/store/library';
import applicant from './vuex/store/applicant';
import directory from './vuex/store/directory';
import events from './vuex/store/events';
import inst_schedule from './vuex/store/schedule/instructor';
import visual_schedule from './vuex/store/schedule/visual';
import hx_toolkit from './vuex/store/hx_toolkit';
import oquarter from './vuex/store/oquarter';
import profile from './vuex/store/profile';
import myplan from './vuex/store/myplan';
import textbooks from './vuex/store/textbooks';
import studSchedule from './vuex/store/schedule/student';
import academicEvents from './vuex/store/academic_events';
import resources from './vuex/store/resources';

vueConf.store.registerModule('notices', notices);
vueConf.store.registerModule('hfs', hfs);
vueConf.store.registerModule('library', library);
vueConf.store.registerModule('applicant', applicant);
vueConf.store.registerModule('directory', directory);
vueConf.store.registerModule('events', events);
vueConf.store.registerModule('visual_schedule', visual_schedule);
vueConf.store.registerModule('hx_toolkit', hx_toolkit);
vueConf.store.registerModule('quicklinks', quicklinks);
vueConf.store.registerModule('oquarter', oquarter);
vueConf.store.registerModule('profile', profile);
vueConf.store.registerModule('myplan', myplan);
vueConf.store.registerModule('textbooks', textbooks);
vueConf.store.registerModule('stud_schedule', studSchedule);
vueConf.store.registerModule('inst_schedule', inst_schedule);
vueConf.store.registerModule('academic_events', academicEvents);
vueConf.store.registerModule('resources', resources);

vueConf.store.commit('addVarToState', {
  name: 'page',
  value: {
    hideTitle: true,
    title: 'Home',
  },
});

Vue.component('myuw-boilerplate', Boilerplate);
Vue.component('myuw-banner-summaries', Summaries);
Vue.component('myuw-notice-card', Notices);
Vue.component('myuw-acad-cal-snippet', AcadCalSnippet);
Vue.component('myuw-ns-critical-info', CriticalInfo);
Vue.component('myuw-ns-international-student', NewInterStudent);
Vue.component('myuw-applicant-cards', Applicant);
Vue.component('myuw-international-student', InterStudent);
Vue.component('myuw-retiree', Retiree);
Vue.component('myuw-events', Events);
Vue.component('myuw-grades', Grades);
Vue.component('myuw-husky-experience', HuskyExperience);
Vue.component('myuw-outage', Outage);
Vue.component('myuw-quicklinks', Quicklinks);
Vue.component('myuw-summer-efs', SummerEfs);
Vue.component('myuw-ns-thank-you', ThankYou);
Vue.component('myuw-ns-to-register', ToRegister);
Vue.component('myuw-reg-status', RegStatus);
Vue.component('myuw-future-quarter-cards', FutureQuarterCards);
Vue.component('myuw-teaching-course-summary', InstructorCourseSummery);
Vue.component('myuw-visual-schedule', VisualSchedule);
Vue.component('myuw-textbooks', Textbooks);
Vue.component('myuw-uwnetid', UWNetID);
Vue.component('myuw-transcripts', Transcripts);
Vue.component('myuw-continuing-education', ContinuingEducation);
Vue.component('myuw-alumni', Alumni);
Vue.component('myuw-hr-payroll', HRPayroll);
Vue.component('myuw-pinned-resources', PinnedResourceCards);
Vue.component('myuw-resource-explore', ResourceExplore);
Vue.component('myuw-grad-pre-application', GraduationPreApplication);

new Vue({
  ...vueConf,
});
