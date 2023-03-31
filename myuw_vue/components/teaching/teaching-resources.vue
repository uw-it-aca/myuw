<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <uw-sidelink-section
        category-title="Course Materials"
        :links="courseMaterialLinks"
      />
      <uw-sidelink-section
        category-title="Web Tools &amp; Services"
        :links="webToolsLinks"
      />
      <uw-sidelink-section
        category-title="Teaching Strategies"
        :links="helpLinks"
      />
    </template>
  </uw-panel>
</template>

<script>
import {mapState} from 'vuex';
import Panel from '../_templates/panel.vue';
import SidelinkSection from '../_templates/sidelink-section.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-sidelink-section': SidelinkSection,
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
      remoteTeachingLinks() {
        return [
          { url: "https://teachingremotely.washington.edu/",
            title: "Teaching Remotely" },
          this.bothell_emp ?
            { url: "https://www.uwb.edu/it/teaching",
              title: "UWB Teach Anywhere" } : null,
          this.tacoma_emp ?
            { url: "https://www.tacoma.uw.edu/uwt/digital-learning/instructional-continuity",
              title: "UWT Instructional Continuity" } : null,
          { url: "https://canvas.uw.edu/courses/1392969",
            title: "Teaching with UW Technologies" },
          { url: "https://teachingremotely.washington.edu/#getHelp",
            title: "Workshops and Office Hours" },
          { url: "https://washington.zoom.us/", title: "Zoom" },
          { url: "https://uw.hosted.panopto.com/", title: "Panopto" },
          { url: "http://polleverywhere.com/", title: "Poll Everywhere" }
        ].filter(x => x !== null);
      },
      courseMaterialLinks() {
        return [
          { url: "http://www2.bookstore.washington.edu/textsys/TextReqLogin.taf?school=" + this.linkData.textbook,
            title: "Order Textbooks" },
          { url: "http://www.lib.washington.edu/types/course",
            title: "Course Reserves" },
          { url: "http://f2.washington.edu/fm/c2/printing-copying/course-packs",
            title: "Request Course Packs" }
        ];
      },
      webToolsLinks() {
        return [
          { url: "http://canvas.uw.edu", title: "Canvas" },
          { url: "https://uw.hosted.panopto.com", title: "Panopto Lecture Capture" },
          { url: "http://www.polleverywhere.com/auth/washington", title: "Poll Everywhere" },
          { url: "https://gradepage.uw.edu", title: "GradePage" },
          { url: "https://apps.registrar.washington.edu/grade-change/pages/change.php",
            title: "Change Submitted Grades" },
          { url: this.linkData.courseEval, title: "Course Evaluations" },
          { url: "https://coda.uw.edu", title: "Course Statistics Dashboard" },
          { url: "https://gsuite.google.com/dashboard", title: "Google Apps" },
          { url: "https://www.office.com/", title: "Office 365 Apps" },
          { url: "https://washington.zoom.us/", title: "Zoom" }
        ];
      },
      helpLinks() {
        return [
          { url: "https://teaching.washington.edu/", title: "Center for Teaching and Learning" },
          { url: "https://teaching.washington.edu/topics/preparing-to-teach/",
            title: "Course and Syllabus Design" },
          { url: "https://teaching.washington.edu/topics/inclusive-teaching/inclusive-teaching-strategies/",
            title: "Inclusive Teaching" },
          { url: "https://teaching.washington.edu/topics/engaging-students-in-learning/",
            title: "Engagement Strategies" },
          { url: "https://teaching.washington.edu/topics/preparing-to-teach/designing-and-refining-hybrid-and-online-courses/",
            title: "Hybrid and Online Course Design" },
        ];
      }
    }),
  },
};
</script>
