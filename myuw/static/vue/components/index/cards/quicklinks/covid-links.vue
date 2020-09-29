<template>
  <div>
    <div>
      <h4>UW Coronavirus</h4>
      <ul v-if="links.student">
        <li>
          <a href="https://www.washington.edu/coronavirus/autumnquarter/">
            Autumn Quarter FAQs
          </a>
        </li>
        <li>
          <a href="https://www.washington.edu/coronavirus/students/">
            Resources for Students
          </a>
        </li>
        <li v-if="links.sea_student">
          <a href="https://wellbeing.uw.edu/">
            Husky Health &amp; Wellbeing
          </a>
        </li>
        <li v-if="links.bot_student">
          <a href="https://www.uwb.edu/studentaffairs/counseling">
            Counseling Center
          </a>
        </li>
        <li v-if="links.tac_student">
          <a href="https://www.tacoma.uw.edu/studentcounseling">
            Counseling &amp; Psychological Services
          </a>
        </li>
        <li>
          <a href="https://www.washington.edu/counseling/covid-19/">
            Coping with COVID-19 Stress
          </a>
        </li>
      </ul>
      <ul v-else>
        <li>
          <a href="https://www.washington.edu/coronavirus/">
            UW Coronavirus Home
          </a>
        </li>
      </ul>
    </div>
    <div v-if="links.student">
      <hr>
      <h4>Remote Learning</h4>
      <ul v-if="links.sea_student">
        <li>
          <a href="https://webster.uaa.washington.edu/asp/website/online-learning/">
            Online Learning Tips and Resources
          </a>
        </li>
      </ul>
      <ul v-if="links.bot_student">
        <li>
          <a href="https://www.uwb.edu/it/student-continuity">
            Student Help for Learning Online
          </a>
        </li>
        <li>
          <a href="https://www.uwb.edu/diversity/diversity-center/firstgenstudents/student-resources/academicsupport">
            Academic Support Services
          </a>
        </li>
        <li>
          <a href="https://www.uwb.edu/it/service-catalog/teaching-learning/tech-lending-program">
            Laptop and WiFi Hotspot Lending Program
          </a>
        </li>
      </ul>
      <ul v-if="links.tac_student">
        <li>
          <a href="https://www.tacoma.uw.edu/digital-learning/student-online-support">
            Online Learning Support
          </a>
        </li>
        <li>
          <a href="https://www.tacoma.uw.edu/teaching-learning-center/teaching-learning-center">
            Teaching and Learning Center
          </a>
        </li>
        <li>
          <a href="https://www.tacoma.uw.edu/information-technology/equipment-checkout">
            Equipment Checkout
          </a>
        </li>
      </ul>
    </div>
    <div v-if="links.instructor">
      <hr>
      <h4>Remote Teaching</h4>
      <ul>
        <li>
          <a href="https://teachingremotely.washington.edu/">
            Teaching Remotely
          </a>
          <span>Plan and deliver high-quality remote learning</span>
        </li>
        <li v-if="links.bot_emp">
          <a href="https://www.uwb.edu/it/teaching">
            UWB Teach Anywhere
          </a>
          <span>UW Bothell resources for teaching online</span>
        </li>
        <li v-if="links.tac_emp">
          <a href="https://www.tacoma.uw.edu/digital-learning/instructional-continuity">
            UWT Instructional Continuity
          </a>
          <span>UW Tacoma resources for teaching online</span>
        </li>
        <li>
          <a href="https://canvas.uw.edu/courses/1392969">
            Teaching with UW Technologies
          </a>
          <span>Learn about technology to support online instruction</span>
        </li>
        <li>
          <a href="https://teachingremotely.washington.edu/#getHelp">
            Workshops and Office Hours
          </a>
          <span>
            Calendars for workshops and office hours for all three campuses
          </span>
        </li>
        <li>
          <a href="https://washington.zoom.us/">Zoom</a>
          <span>Schedule and start online class sessions.</span>
        </li>
        <li>
          <a href="https://panopto.uw.edu/">Panopto</a>
          <span>Lecture capture – record, schedule, and review lectures</span>
        </li>
        <li>
          <a href="http://polleverywhere.com/">Poll Everywhere</a>
          <span>Create poll responses for your classes</span>
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
