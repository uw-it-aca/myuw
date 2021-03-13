<template>
  <div>
    <h4 class="h6 font-weight-bold">
      Visa and Immigration Rules
    </h4>
    <ul class="mb-4 list-unstyled myuw-text-md">
      <li>
        <a
          href="https://iss.washington.edu/travel-visas/"
          target="_blank"
          label="Travel and Visas for Int'l Students"
        >Travel and Visas</a>
      </li>
      <li>
        <a
          v-if="visaJ1"
          href="https://iss.washington.edu/regulations/j1/"
          target="_blank"
          label="Visa and Immigration Rules"
        >Visa and Immigration Rules for J-1 students</a>
        <a
          v-else
          href="https://iss.washington.edu/regulations/f1/"
          target="_blank"
          label="Visa and Immigration Rules"
        >Visa and Immigration Rules for F-1 students</a>
      </li>
      <li>
        <a
          href="https://iss.washington.edu/new-students/faq/"
          target="_blank"
          label="ISS: Frequently Asked Questions (FAQ)"
        >Frequently Asked Questions (FAQ)</a>
      </li>
      <li>
        <a
          href="https://iss.washington.edu/employment/"
          target="_blank"
          label="Int'l Student Employment"
        >Employment and Internships</a>
      </li>
      <li>
        <a
          href="https://www.trumba.com/calendars/sea_enroll-iss"
          target="_blank"
          label="Deadlines and Workshops Calendar"
        >Deadlines and Workshops Calendar</a>
      </li>
    </ul>

    <h4 class="h6 font-weight-bold">
      Academic Support
    </h4>
    <ul class="mb-4 list-unstyled myuw-text-md">
      <li>
        <a
          href="http://depts.washington.edu/aspuw/clue/home/"
          target="_blank"
          label="Center for Learning and Undergraduate Enrichment (CLUE)"
        >Center for Learning and Undergraduate Enrichment (CLUE)</a>
      </li>
      <li>
        <a
          href="http://depts.washington.edu/owrc"
          target="_blank"
          label="Odegaard Writing and Research Center"
        >Odegaard Writing and Research Center</a>
      </li>
      <li>
        <a
          href="http://aep.washington.edu/"
          target="_blank"
          label="Academic English Program"
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
