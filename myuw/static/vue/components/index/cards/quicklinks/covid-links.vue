<template>
  <div class="mx-n3 mb-3 p-3 myuw-covid-links">
    <div>
      <h4 class="h6">
        UW Coronavirus
      </h4>
      <ul v-if="links.student" class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="https://www.washington.edu/coronavirus/autumnquarter/">
            Autumn Quarter FAQs
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/coronavirus/students/">
            Resources for Students
          </a>
        </li>
        <li v-if="links.sea_student" class="mb-1">
          <a href="https://wellbeing.uw.edu/">
            Husky Health &amp; Wellbeing
          </a>
        </li>
        <li v-if="links.bot_student" class="mb-1">
          <a href="https://www.uwb.edu/studentaffairs/counseling">
            Counseling Center
          </a>
        </li>
        <li v-if="links.tac_student" class="mb-1">
          <a href="https://www.tacoma.uw.edu/studentcounseling">
            Counseling &amp; Psychological Services
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/counseling/covid-19/">
            Coping with COVID-19 Stress
          </a>
        </li>
      </ul>
      <ul v-else class="list-unstyled mb-0 myuw-text-md">
        <li class="mb-1">
          <a href="https://www.washington.edu/coronavirus/">
            UW Coronavirus Home
          </a>
        </li>
      </ul>
    </div>
    <div v-if="links.student">
      <hr>
      <h4 class="h6">
        Remote Learning
      </h4>
      <ul v-if="links.sea_student" class="list-unstyled mb-0 myuw-text-md">
        <li class="mb-1">
          <a href="https://webster.uaa.washington.edu/asp/website/online-learning/">
            Online Learning Tips and Resources
          </a>
        </li>
      </ul>
      <ul v-if="links.bot_student">
        <li class="mb-1">
          <a href="https://www.uwb.edu/it/student-continuity">
            Student Help for Learning Online
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.uwb.edu/diversity/diversity-center/firstgenstudents/student-resources/academicsupport">
            Academic Support Services
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.uwb.edu/it/service-catalog/teaching-learning/tech-lending-program">
            Laptop and WiFi Hotspot Lending Program
          </a>
        </li>
      </ul>
      <ul v-if="links.tac_student">
        <li class="mb-1">
          <a href="https://www.tacoma.uw.edu/digital-learning/student-online-support">
            Online Learning Support
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.tacoma.uw.edu/teaching-learning-center/teaching-learning-center">
            Teaching and Learning Center
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.tacoma.uw.edu/information-technology/equipment-checkout">
            Equipment Checkout
          </a>
        </li>
      </ul>
    </div>
    <div v-if="links.instructor">
      <hr>
      <h4 class="h6">
        Remote Teaching
      </h4>
      <ul class="list-unstyled mb-0 myuw-text-md">
        <li class="mb-2">
          <a href="https://teachingremotely.washington.edu/">
            Teaching Remotely
          </a>
          <div class="font-weight-light myuw-text-sm">
            Plan and deliver high-quality remote learning
          </div>
        </li>
        <li v-if="links.bot_emp" class="mb-2">
          <a href="https://www.uwb.edu/it/teaching">
            UWB Teach Anywhere
          </a>
          <div class="font-weight-light myuw-text-sm">
            UW Bothell resources for teaching online
          </div>
        </li>
        <li v-if="links.tac_emp" class="mb-2">
          <a href="https://www.tacoma.uw.edu/digital-learning/instructional-continuity">
            UWT Instructional Continuity
          </a>
          <div class="font-weight-light myuw-text-sm">
            UW Tacoma resources for teaching online
          </div>
        </li>
        <li class="mb-2">
          <a href="https://canvas.uw.edu/courses/1392969">
            Teaching with UW Technologies
          </a>
          <div class="font-weight-light myuw-text-sm">
            Learn about technology to support online instruction
          </div>
        </li>
        <li class="mb-2">
          <a href="https://teachingremotely.washington.edu/#getHelp">
            Workshops and Office Hours
          </a>
          <div class="font-weight-light myuw-text-sm">
            Calendars for workshops and office hours for all three campuses
          </div>
        </li>
        <li class="mb-2">
          <a href="https://washington.zoom.us/">Zoom</a>
          <div class="font-weight-light myuw-text-sm">
            Schedule and start online class sessions
          </div>
        </li>
        <li class="mb-2">
          <a href="https://panopto.uw.edu/">Panopto</a>
          <div class="font-weight-light myuw-text-sm">
            Lecture capture – record, schedule, and review lectures
          </div>
        </li>
        <li class="mb-2">
          <a href="http://polleverywhere.com/">Poll Everywhere</a>
          <div class="font-weight-light myuw-text-sm">
            Create poll responses for your classes
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    links: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../../css/myuw/variables.scss";

.myuw-covid-links {
  background-color: lighten(map.get($theme-colors, "beige"), 7%) !important;
}

</style>
