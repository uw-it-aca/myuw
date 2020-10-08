<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h3 class="text-dark-beige">
        Your Returning Student Application
      </h3>
    </template>
    <template v-else #card-heading>
      <h3 class="text-dark-beige">
        Your Bothell Application for
        {{ ucfirst(applicantData.quarter) }} {{ applicantData.year }}
      </h3>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h4 class="h5 mb-3 text-dark-beige">
        For application status, contact the UW Bothell Office of Admissions
      </h4>
      <b-container>
        <b-row>
          <b-col>Email</b-col>
          <b-col><a href="mailto:uwbifo@uw.edu">uwbifo@uw.edu</a></b-col>
        </b-row>
        <b-row>
          <b-col>Phone</b-col>
          <b-col>(425) 352-5000</b-col>
        </b-row>
        <b-row>
          <b-col>Mail</b-col>
          <b-col>10909 NE 185th St <br>Bothell, WA 98011<br>Box 358500</b-col>
        </b-row>
      </b-container>
      <h4 class="h5 mb-3 text-dark-beige">
        Resources for Bothell Applicants
      </h4>
      <ul class="list-unstyled myuw-text-md">
        <li>
          <a href="http://www.uwb.edu/financialaid"
             target="_blank" aria-label="Student Financial Aid"
          >
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li>
          <a href="http://www.uwb.edu/studentaffairs"
             target="_blank" aria-label="Student Resources"
          >
            Check out the student resources for student life,
            career services, and more
          </a>
        </li>
        <li>
          <a href="http://www.uwb.edu/calendars"
             target="_blank" aria-label="UW Bothell Academic calendars"
          >
            View the UW Bothell Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <a class="btn btn-outline-secondary text-dark my-4" href="https://admissions.uwb.edu/apply/status"
         aria-label="Your application status details"
      >
        View your {{ applicantData.type }} application status and checklist
      </a>
      <p>
        If you have questions regarding your application,
        please contact UW Bothell Office of Admissions at
        <a href="mailto:uwbinfo@uw.edu">uwbinfo@uw.edu</a>
      </p>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    applicantData: {
      type: [Object, Boolean],
      default: false,
    },
    isReady: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

