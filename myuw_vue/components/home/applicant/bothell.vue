<template>
  <uw-card v-if="!isReady || applicantData" :loaded="isReady">
    <template v-if="isReturning" #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Returning Student Form
      </h2>
    </template>
    <template v-else #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Bothell Application for
        {{ titleCaseWord(applicantData.quarter) }} {{ applicantData.year }}
      </h2>
    </template>
    <template v-if="isReturning" #card-body>
      <h3 class="h6 myuw-font-encode-sans">
        Form status
      </h3>
      <p class="myuw-text-md">
        For returning student form status, contact the UW Bothell Office of the Registrar:
      </p>
      <div class="container mb-3 myuw-text-md">
        <div class="d-flex">
          <div class="me-5">Email</div>
          <div><a href="mailto:uwbreg@uw.edu">uwbreg@uw.edu</a></div>
        </div>
        <div class="d-flex">
          <div class="me-3 pe-4">Phone</div>
          <div>(425) 352-5000</div>
        </div>
        <div class="d-flex">
          <div class="me-4 pe-1">Location</div>
          <div>Husky Hall<br />10909 NE 185th St <br />Bothell, WA 98011</div>
        </div>
      </div>

      <h3 class="h6 myuw-font-encode-sans">Registration for returning student</h3>
      <ul class="list-style myuw-text-md">
        <li>
          You must
          <a href="https://sdb.admin.uw.edu/enroll/uwnetid/">confirm your enrollment</a>
          and pay the enrollment fee prior to being able to register.
        </li>
        <li>
          You will then register beginning with Registration Period II for your returning quarter.
          Check dates on the
          <a href="http://www.uwb.edu/calendars">Academic Calendar</a>.
        </li>
      </ul>

      <h3 class="h6 myuw-font-encode-sans">
        Resources for Bothell applicants
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
  computed: {
    isReturning() {
      return this.applicantData.is_returning;
    }
  },
};
</script>
