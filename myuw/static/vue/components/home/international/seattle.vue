<template>
  <div>
    <h3 class="h6 font-weight-bold">
      Visa and Immigration Rules
    </h3>
    <ul class="mb-4 list-unstyled myuw-text-md">
      <li>
        <a
          v-out="'ISS: Travel and Visas'"
          href="https://iss.washington.edu/travel-visas/"
          target="_blank"
        >Travel and Visas</a>
      </li>
      <li>
        <a
          v-if="visaJ1"
          href="https://iss.washington.edu/regulations/j1/"
          target="_blank"
        >Visa and Immigration Rules for J-1 students</a>
        <a
          v-else
          href="https://iss.washington.edu/regulations/f1/"
          target="_blank"
        >Visa and Immigration Rules for F-1 students</a>
      </li>
      <li>
        <a
          v-out="'ISS: Frequently Asked Questions'"
          href="https://iss.washington.edu/new-students/faq/"
          target="_blank"
        >Frequently Asked Questions (FAQ)</a>
      </li>
      <li>
        <a
          v-out="'ISS: Student Employment'"
          href="https://iss.washington.edu/employment/"
          target="_blank"
        >Employment and Internships</a>
      </li>
      <li>
        <a
          href="https://www.trumba.com/calendars/sea_enroll-iss"
          target="_blank"
        >Deadlines and Workshops Calendar</a>
      </li>
    </ul>

    <h3 class="h6 font-weight-bold">
      Academic Support
    </h3>
    <ul class="mb-4 list-unstyled myuw-text-md">
      <li>
        <a
          href="http://depts.washington.edu/aspuw/clue/home/"
          target="_blank"
        >Center for Learning and Undergraduate Enrichment (CLUE)</a>
      </li>
      <li>
        <a
          href="http://depts.washington.edu/owrc"
          target="_blank"
        >Odegaard Writing and Research Center</a>
      </li>
      <li>
        <a
          href="http://aep.washington.edu/"
          target="_blank"
        >Academic English Program</a>
      </li>
    </ul>

    <h4 class="h6 font-weight-bold">
      Social Events
    </h4>
    <ul class="mb-4 list-unstyled myuw-text-md">
      <li>
        <a href="https://www.washington.edu/circle/calendar/"
          target="_blank"
        >
          CIRCLE Events Calendar
        </a>
      </li>
      <li>
        <a
          href="https://www.washington.edu/circle/calendar/"
          target="_blank"
        >CIRCLE Events Calendar</a>
      </li>
      <li>
        <a
          href="http://www.fiuts.org/events"
          target="_blank"
        >FIUTS Event Calendar</a>
      </li>
    </ul>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  computed: mapState({
    visaJ1: (state) => state.user.affiliations.J1,
  }),
};
</script>
