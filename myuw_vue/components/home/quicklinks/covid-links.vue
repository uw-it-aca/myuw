<template>
  <div class="mx-n3 mb-3 p-3 myuw-covid-links">
    <div v-if="student">
      <h3 class="h6">
        UW Coronavirus
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a href="https://www.washington.edu/coronavirus/">
            UW Coronavirus Home
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/coronavirus/students/">
            Resources for Students
          </a>
        </li>
        <li v-if="seattleStudent" class="mb-1">
          <a href="https://wellbeing.uw.edu/">
            Husky Health &amp; Wellbeing
          </a>
        </li>
        <li v-if="bothellStudent" class="mb-1">
          <a href="https://www.uwb.edu/studentaffairs/counseling">
            Counseling Center
          </a>
        </li>
        <li v-if="tacomaStudent" class="mb-1">
          <a href="https://www.tacoma.uw.edu/studentcounseling">
            Counseling &amp; Psychological Services
          </a>
        </li>
        <li v-if="tacomaStudent" class="mb-1">
          <a href="https://apps.tacoma.uw.edu/attest/">
            Student Wellness Check-In
          </a>
        </li>
        <li class="mb-1">
          <a href="https://www.washington.edu/counseling/covid-19/">
            Coping with COVID-19 Stress
          </a>
        </li>
      </ul>
    </div>
    <div v-if="seattleStudent || bothellStudent || tacomaStudent">
      <hr class="bg-secondary">
      <h3 class="h6">
        Online Learning
      </h3>
      <ul v-if="seattleStudent" class="list-unstyled mb-0 myuw-text-md">
        <li class="mb-1">
          <a href="https://webster.uaa.washington.edu/asp/website/online-learning/">
            Online Learning Tips and Resources
          </a>
        </li>
      </ul>
      <ul v-if="bothellStudent" class="list-unstyled mb-0 myuw-text-md">
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
      <ul v-if="tacomaStudent" class="list-unstyled mb-0 myuw-text-md">
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
    <div v-if="instructor">
      <p class="myuw-text-sm">
        Zoom now has a permanent spot in the Quick Links above.
        You can add other links by customizing your Quick Links,
        including adding recently visited links from below.
      </p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      instructor: (state) => state.user.affiliations.instructor,
      seattleStudent: (state) => state.user.affiliations.seattle,
      bothellStudent: (state) => state.user.affiliations.bothell,
      tacomaStudent: (state) => state.user.affiliations.tacoma,
      seattleEmp: (state) => state.user.affiliations.official_seattle,
      bothellEmp: (state) => state.user.affiliations.official_bothell,
      tacomaEmp: (state) => state.user.affiliations.official_tacoma,
    }),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';

.myuw-covid-links {
  background-color: lighten(map.get($theme-colors, "beige"), 10%) !important;
}

</style>
