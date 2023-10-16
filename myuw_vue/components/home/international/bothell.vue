<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">CIE Portal</h3>
    <p class="myuw-text-md">
      Use CIE Portal to create requests, maintain your immigration record, report required
      immigration information to the U.S. government, and get critical updates about visa status.
      <br />
      <uw-link-button class="mt-2 mb-1" href="https://cie.uwb.edu">
        Go to CIE Portal
      </uw-link-button>
    </p>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Visa and Immigration Rules</h3>

    <ul class="list-unstyled myuw-text-md">
      <li class="mb-1">
        <a href="https://www.uwb.edu/international-student-services/alumni/travel">Travel and Visas</a>
      </li>
      <li class="mb-1">
        <a href="https://www.uwb.edu/international-student-services/next-steps/arrival"
          >Immigration Document for F-1 Students</a
        >
      </li>
      <li class="mb-1">
        <a href="https://www.uwb.edu/international-student-services/current-students/vacation-quarter">Vacation Quarter</a>
      </li>
      <li class="mb-1">
        <a href="https://www.uwb.edu/international-student-services/current-students/employment">Employment</a>
      </li>
      <li class="mb-1">
        <a href="https://www.uwb.edu/cie/events"
          >Center for International Education (CIE) Calendar</a
        >
      </li>
    </ul>

    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Academic Support</h3>
    <ul class="list-unstyled myuw-text-md mb-2">
      <li class="mb-1">
        <a href="https://www.uwb.edu/international-student-services/current-students/writing-support"
          >Writing Support</a
        >
      </li>
      <li class="mb-1">
        <a href="https://www.uwb.edu/academic-support-programs/wacc">Writing and Communication Center (WaCC)</a>
      </li>
      <li>
        <a href="https://www.uwb.edu/qsc">Quantitative Skills Center (QSC)</a>
      </li>
    </ul>
  </div>
</template>

<script>
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-link-button': LinkButton,
  },
};
</script>
