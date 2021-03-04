<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <div>
        <h3 class="h5">
          Remote Teaching
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://teachingremotely.washington.edu/" label="">Teaching Remotely</a>
          </li>
          <!-- BOTHELL ONLY --->
          <li v-if="bothell_emp" class="mb-1">
            <a href="https://www.uwb.edu/it/teaching" label="">UWB Teach Anywhere</a>
          </li>
          <!-- TACOMA ONLY --->
          <li v-if="tacoma_emp" class="mb-1">
            <a href="https://www.tacoma.uw.edu/digital-learning/instructional-continuity"
              label="">UWT Instructional Continuity</a>
          </li>
          <li class="mb-1">
            <a href="https://canvas.uw.edu/courses/1392969"
              label="">Teaching with UW Technologies</a>
          </li>
          <li class="mb-1">
            <a href="https://teachingremotely.washington.edu/#getHelp"
              label="">Workshops and Office Hours</a>
          </li>
          <li class="mb-1">
            <a href="https://washington.zoom.us/" label="">Zoom</a>
          </li>
          <li class="mb-1">
            <a href="https://panopto.uw.edu/" label="">Panopto</a>
          </li>
          <li>
            <a href="http://polleverywhere.com/" label="">Poll Everywhere</a>
          </li>
        </ul>

        <h3 class="h5">
          Course Materials
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a :href="'http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=' + linkData.textbook"
              label="">Order Textbooks</a>
            </li>
          <li class="mb-1">
            <a href="http://www.lib.washington.edu/types/course" label="">Course Reserves</a>
          </li>
          <li>
            <a href="http://f2.washington.edu/fm/c2/printing-copying/course-packs" label="">Request Course Packs</a>
          </li>
        </ul>
        <h3 class="h5">
          Web Tools &amp; Services
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="http://canvas.uw.edu" label="">Canvas</a>
          </li>
          <li class="mb-1">
            <a href="https://panopto.uw.edu" label="">Panopto Lecture Capture</a>
          </li>
          <li class="mb-1">
            <a href="http://www.polleverywhere.com/auth/washington" label="">Poll Everywhere</a></li>
          <li class="mb-1">
            <a href="https://gradepage.uw.edu" label="">GradePage</a>
          </li>
          <li class="mb-1">
            <a href="https://apps.registrar.washington.edu/grade-change/pages/change.php" label="">Change Submitted Grades</a>
          </li>
          <li class="mb-1">
            <a :href="linkData.courseEval" label="">Course Evaluations</a>
          </li>
          <li>
            <a href="https://coda.uw.edu" label="">Course Stats</a>
          </li>
        </ul>
        <h3 class="h5">
          Help Guides
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://itconnect.uw.edu/learn/tools/" label="">Teaching &amp; Learning Tools</a>
            </li>
          <li class="mb-1">
            <a href="http://www.washington.edu/teaching/" label="">Center for Teaching &amp; Learning</a>
            </li>
          <li class="mb-1">
            <a href="http://depts.washington.edu/grading/" label="">Faculty Resources on Grading</a>
            </li>
          <li class="mb-1">
            <a href="https://itconnect.uw.edu/learn/tools/gradepage/assign-submit-grades/"
              label="">Online Grade Submission</a></li>
          <li>
            <a href="http://teaching.pce.uw.edu/" label="">UW PCE Instructor Resources</a>
          </li>
        </ul>
      </div>
    </template>
  </uw-panel>
</template>

<script>
import {mapState} from 'vuex';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
  },
  computed: {
    ...mapState({
      seattle_emp: (state) => state.user.affiliations.official_seattle,
      bothell_emp: (state) => state.user.affiliations.official_bothell,
      tacoma_emp: (state) => state.user.affiliations.official_tacoma,
      linkData() {
        let textbookLink = '';
        let courseEvalLink = '';
        if (this.bothell_emp) {
          textbookLink = 'uwbothell';
          courseEvalLink = 'https://uwb.iasystem.org/faculty';
        } else if (this.tacoma_emp) {
          textbookLink = 'uwtacoma';
          courseEvalLink = 'https://uwt.iasystem.org/faculty';
        } else if (this.seattle_emp) {
          textbookLink = 'uwmain';
          courseEvalLink = 'https://uw.iasystem.org/faculty';
        } else {
          textbookLink = 'uwmain';
          courseEvalLink = 'https://www.washington.edu/assessment/course-evaluations/';
        }
        return {
          textbook: textbookLink,
          courseEval: courseEvalLink,
        };
      },
    }),
  },
};
</script>
