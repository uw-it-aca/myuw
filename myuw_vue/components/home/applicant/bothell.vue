<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="applicantData.is_returning" #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Application
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Bothell Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="applicantData.is_returning" #card-body>
      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        For application status, contact the UW Bothell Office of Admissions
      </h3>
      <div class="container">
        <div class="row">
          <div class="col">Email</div>
          <div class="col"><a href="mailto:uwbifo@uw.edu">uwbifo@uw.edu</a></div>
        </div>
        <div class="row">
          <div class="col">Phone</div>
          <div class="col">(425) 352-5000</div>
        </div>
        <div class="row">
          <div class="col">Mail</div>
          <div class="col">10909 NE 185th St <br />Bothell, WA 98011<br />Box 358500</div>
        </div>
      </div>

      <h3 class="h6 text-dark-beige myuw-font-encode-sans">
        Resources for Bothell Applicants
      </h3>
      <ul class="list-unstyled myuw-text-md">
        <li class="mb-1">
          <a v-out="'UW Bothell Student Financial Aid'" href="http://www.uwb.edu/financialaid">
            Learn all about student financial aid and scholarships
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Bothell Student Resources'" href="http://www.uwb.edu/studentaffairs">
            Check out the student resources for student life, career services, and more
          </a>
        </li>
        <li class="mb-1">
          <a v-out="'UW Bothell Academic calendars'" href="http://www.uwb.edu/calendars">
            View the UW Bothell Academic calendars
          </a>
        </li>
      </ul>
    </template>
    <template v-else #card-body>
      <uw-link-button class="my-4" href="https://admissions.uwb.edu/apply/status">
        View your {{ applicantData.type }} application status and checklist
      </uw-link-button>
      <p>
        If you have questions regarding your application, please contact UW Bothell Office of
        Admissions at
        <a v-out="'Contact UWB'" href="mailto:uwbinfo@uw.edu">uwbinfo@uw.edu</a>
      </p>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton,
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
