<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">MyISSS</h3>
    <p class="myuw-text-md">
      Use MyISSS to create requests, maintain your immigration record, report required immigration
      information to the U.S. government, and get critical updates about visa status. <br>
      <uw-link-button class="mt-2 mb-1" href="https://isss.uw.edu/"> Go to MyISSS </uw-link-button>
    </p>

    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Visa and Immigration Rules</h3>
    <ul class="list-unstyled myuw-text-md">
      <li class="mb-1">
        <a v-out="'ISS: Travel and Visas'" href="https://iss.washington.edu/travel-visas/"
          >Travel and Visas</a
        >
      </li>
      <li class="mb-1">
        <a v-if="visaJ1" href="https://iss.washington.edu/regulations/j1/"
          >Visa and Immigration Rules for J-1 students</a
        >
        <a v-else href="https://iss.washington.edu/regulations/f1/"
          >Visa and Immigration Rules for F-1 students</a
        >
      </li>
      <li class="mb-1">
        <a
          v-out="'ISS: Frequently Asked Questions'"
          href="https://iss.washington.edu/new-students/faq/"
          >Frequently Asked Questions (FAQ)</a
        >
      </li>
      <li class="mb-1">
        <a v-out="'ISS: Student Employment'" href="https://iss.washington.edu/employment/"
          >Employment and Internships</a
        >
      </li>
      <li class="mb-1">
        <a href="https://www.trumba.com/calendars/sea_enroll-iss"
          >Deadlines and Workshops Calendar</a
        >
      </li>
    </ul>

    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Academic Support</h3>
    <ul class="list-unstyled myuw-text-md">
      <li class="mb-1">
        <a href="https://depts.washington.edu/aspuw/clue/home/"
          >Center for Learning and Undergraduate Enrichment (CLUE)</a
        >
      </li>
      <li class="mb-1">
        <a href="https://depts.washington.edu/owrc">Odegaard Writing and Research Center</a>
      </li>
      <li class="mb-1">
        <a href="https://aep.washington.edu/">Academic English Program</a>
      </li>
    </ul>

    <h3 class="h6 text-dark-beige myuw-font-encode-sans">Social Events</h3>
    <ul class="list-unstyled myuw-text-md mb-2">
      <li class="mb-1">
        <a href="https://www.washington.edu/circle/calendar/">CIRCLE Events Calendar</a>
      </li>
      <li>
        <a href="https://www.fiuts.org/events">FIUTS Event Calendar</a>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import LinkButton from '../../_templates/link-button.vue';

export default {
  components: {
    'uw-link-button': LinkButton,
  },
  computed: mapState({
    visaJ1: (state) => state.user.affiliations.J1,
  }),
};
</script>
