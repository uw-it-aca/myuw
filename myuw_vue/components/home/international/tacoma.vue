<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">ISSS Portal</h3>
    <p class="myuw-text-md">
      Use ISSS Portal to create requests, maintain your immigration record, report required
      immigration information to the U.S. government, and get critical updates about visa status.
      <br>
      <uw-link-button class="mt-2 mb-1" href="https://isss.tacoma.uw.edu/">
        Go to ISSS Portal
      </uw-link-button>
    </p>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Visa and Immigration Rules</h3>

    <ul class="list-unstyled myuw-text-md">
      <li class="mb-1">
        <a href="https://www.tacoma.uw.edu/uwt/oga/isss-travel-and-visa">Travel and Visas</a>
      </li>
      <li class="mb-1">
        <a href="https://www.tacoma.uw.edu/uwt/oga/isss-maintaining-f1"
          >Rules to maintain F-1 status</a
        >
      </li>
      <li class="mb-1">
        <a href="https://www.tacoma.uw.edu/uwt/oga/isss-employment"
          >International Student Employment</a
        >
      </li>
      <li class="mb-1">
        <a href="https://www.trumba.com/calendars/tac-iss"
          >International Student and Scholar Services (ISSS) Calendar</a
        >
      </li>
    </ul>

    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Academic Support</h3>
    <ul class="list-unstyled myuw-text-md mb-2">
      <li class="mb-1">
        <a href="https://www.tacoma.uw.edu/teaching-and-learning-center/writing-resources-0"
          >Academic Writing Resources</a
        >
      </li>
      <li>
        <a href="https://www.tacoma.uw.edu/teaching-learning-center/teaching-learning-center"
          >Teaching and Learning Center</a
        >
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
