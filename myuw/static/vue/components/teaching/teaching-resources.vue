<template>
  <div>
    <ul class="unstyled-list">
      <li><a href="https://teachingremotely.washington.edu/">Teaching Remotely</a></li>
      <!-- BOTHELL ONLY --->
      <li v-if="bothell_emp"><a href="https://www.uwb.edu/it/teaching">UWB Teach Anywhere</a></li>
      <!-- TACOMA ONLY --->
      <li v-if="tacoma_emp"><a href="https://www.tacoma.uw.edu/digital-learning/instructional-continuity">UWT Instructional Continuity</a></li>
      <li><a href="https://canvas.uw.edu/courses/1392969">Teaching with UW Technologies</a></li>
      <li><a href="https://teachingremotely.washington.edu/#getHelp">Workshops and Office Hours</a></li>
      <li><a href="https://washington.zoom.us/">Zoom</a></li>
      <li><a href="https://panopto.uw.edu/">Panopto</a></li>
      <li><a href="http://polleverywhere.com/">Poll Everywhere</a></li>
    </ul>

    <h3 class="myuw-canvas-title">Course Materials</h3>
      <ul class="unstyled-list">
        <li><a :href="'http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=' + linkData.textbook" rel="">Order Textbooks</a></li>
        <li><a href="http://www.lib.washington.edu/types/course" rel="">Course Reserves</a></li>
        <li><a href="http://f2.washington.edu/fm/c2/printing-copying/course-packs" rel="">Request Course Packs</a></li>
      </ul>
      <h3 class="myuw-canvas-title">Web Tools &amp; Services</h3>
      <ul class="unstyled-list">
        <li><a href="http://canvas.uw.edu" rel="">Canvas</a></li>
        <li><a href="https://panopto.uw.edu" rel="">Panopto Lecture Capture</a></li>
        <li><a href="http://www.polleverywhere.com/auth/washington" rel="">Poll Everywhere</a></li>
        <li><a href="https://gradepage.uw.edu" rel="">GradePage</a></li>
        <li><a href="https://apps.registrar.washington.edu/grade-change/pages/change.php" rel="">Change Submitted Grades</a></li>
        <li><a :href="linkData.courseEval" rel="">Course Evaluations</a></li>
        <li><a href="https://coda.uw.edu" rel="">Course Stats</a></li>
      </ul>
      <h3 class="myuw-canvas-title">Help Guides</h3>
      <ul class="unstyled-list">
        <li><a href="https://itconnect.uw.edu/learn/tools/" rel="">Teaching &amp; Learning Tools</a></li>
        <li><a href="http://www.washington.edu/teaching/" rel="">Center for Teaching &amp; Learning</a></li>
        <li><a href="http://depts.washington.edu/grading/" rel="">Faculty Resources on Grading</a></li>
        <li><a href="https://itconnect.uw.edu/learn/tools/gradepage/assign-submit-grades/" rel="">Online Grade Submission</a></li>
        <li><a href="http://teaching.pce.uw.edu/" rel="">UW PCE Instructor Resources</a></li>
      </ul>
  </div>

</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  computed: {
    ...mapState({
      seattle_emp: (state) => state.user.affiliations.official_seattle,
      bothell_emp: (state) => state.user.affiliations.official_bothell,
      tacoma_emp: (state) => state.user.affiliations.official_tacoma,
      linkData: () => {
        let textbookLink, courseEvalLink = '';
        if (bothell_emp) {
          textbookLink = 'uwbothell';
          courseEvalLink = 'https://uwb.iasystem.org/faculty';
        } else if (tacoma_emp) {
          textbookLink = 'uwtacoma';
          courseEvalLink = 'https://uwt.iasystem.org/faculty';
        } else if (seattle_emp) {
          textbookLink = 'uwmain';
          courseEvalLink = 'https://uw.iasystem.org/faculty'
        } else {
          textbookLink = 'uwmain';
          courseEvalLink = 'https://www.washington.edu/assessment/course-evaluations/';
        };
        return {
          textbook: textbookLink,
          courseEval: courseEvalLink,
        }
      },
    }),
  },
};
</script>
