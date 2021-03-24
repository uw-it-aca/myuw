<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <div>
        <h2 class="h5">
          Remote Teaching
        </h2>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://teachingremotely.washington.edu/">Teaching Remotely</a>
          </li>
          <li v-if="bothell_emp" class="mb-1">
            <a href="https://www.uwb.edu/it/teaching">UWB Teach Anywhere</a>
          </li>
          <li v-if="tacoma_emp" class="mb-1">
            <a href="https://www.tacoma.uw.edu/digital-learning/instructional-continuity"
             >UWT Instructional Continuity</a>
          </li>
          <li class="mb-1">
            <a href="https://canvas.uw.edu/courses/1392969"
             >Teaching with UW Technologies</a>
          </li>
          <li class="mb-1">
            <a href="https://teachingremotely.washington.edu/#getHelp"
             >Workshops and Office Hours</a>
          </li>
          <li class="mb-1">
            <a href="https://washington.zoom.us/">Zoom</a>
          </li>
          <li class="mb-1">
            <a href="https://panopto.uw.edu/">Panopto</a>
          </li>
          <li>
            <a href="http://polleverywhere.com/">Poll Everywhere</a>
          </li>
        </ul>

        <h2 class="h5">
          Course Materials
        </h2>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a :href="'http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=' + linkData.textbook"
             >Order Textbooks</a>
            </li>
          <li class="mb-1">
            <a href="http://www.lib.washington.edu/types/course">Course Reserves</a>
          </li>
          <li>
            <a href="http://f2.washington.edu/fm/c2/printing-copying/course-packs">Request Course Packs</a>
          </li>
        </ul>
        <h2 class="h5">
          Web Tools &amp; Services
        </h2>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="http://canvas.uw.edu">Canvas</a>
          </li>
          <li class="mb-1">
            <a href="https://panopto.uw.edu">Panopto Lecture Capture</a>
          </li>
          <li class="mb-1">
            <a href="http://www.polleverywhere.com/auth/washington">Poll Everywhere</a></li>
          <li class="mb-1">
            <a href="https://gradepage.uw.edu">GradePage</a>
          </li>
          <li class="mb-1">
            <a href="https://apps.registrar.washington.edu/grade-change/pages/change.php">Change Submitted Grades</a>
          </li>
          <li class="mb-1">
            <a :href="linkData.courseEval">Course Evaluations</a>
          </li>
          <li>
            <a href="https://coda.uw.edu">Course Stats</a>
          </li>
        </ul>
        <h2 class="h5">
          Help Guides
        </h2>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://itconnect.uw.edu/learn/tools/">Teaching &amp; Learning Tools</a>
            </li>
          <li class="mb-1">
            <a href="http://www.washington.edu/teaching/">Center for Teaching &amp; Learning</a>
            </li>
          <li class="mb-1">
            <a href="http://depts.washington.edu/grading/">Faculty Resources on Grading</a>
            </li>
          <li class="mb-1">
            <a href="https://itconnect.uw.edu/learn/tools/gradepage/assign-submit-grades/"
             >Online Grade Submission</a></li>
          <li>
            <a href="http://teaching.pce.uw.edu/">UW PCE Instructor Resources</a>
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
