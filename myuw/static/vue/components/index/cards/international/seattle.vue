<template>
  <div>
    <h4 class="h5 myuw-card-header">
      Visa and Immigration Rules
    </h4>
    <ul class="list-unstyled">
      <li>
        <a
          href="https://iss.washington.edu/travel-visas/"
          target="_blank"
          aria-label="Travel and Visas for Int'l Students"
        >Travel and Visas</a>
      </li>
      <li>
        <a
          v-if="user.affiliations.J1"
          href="https://iss.washington.edu/regulations/j1/"
          target="_blank"
          aria-label="Visa and Immigration Rules"
        >Visa and Immigration Rules for J-1 students</a>
        <a
          v-else
          href="https://iss.washington.edu/regulations/f1/"
          target="_blank"
          aria-label="Visa and Immigration Rules"
        >Visa and Immigration Rules for F-1 students</a>
      </li>
      <li>
        <a
          href="https://iss.washington.edu/new-students/faq/"
          target="_blank"
          aria-label="ISS: Frequently Asked Questions (FAQ)"
        >Frequently Asked Questions (FAQ)</a>
      </li>
      <li>
        <a
          href="https://iss.washington.edu/employment/"
          target="_blank"
          aria-label="Int'l Student Employment"
        >Employment and Internships</a>
      </li>
      <li>
        <a
          href="https://www.trumba.com/calendars/sea_enroll-iss"
          target="_blank"
          aria-label="Deadlines and Workshops Calendar"
        >Deadlines and Workshops Calendar</a>
      </li>
    </ul>

    <h4 class="h5 myuw-card-header">
      Academic Support
    </h4>
    <ul class="list-unstyled">
      <li>
        <a
          href="http://depts.washington.edu/aspuw/clue/home/"
          target="_blank"
          aria-label="Center for Learning and Undergraduate Enrichment (CLUE)"
        >Center for Learning and Undergraduate Enrichment (CLUE)</a>
      </li>
      <li>
        <a
          href="http://depts.washington.edu/owrc"
          target="_blank"
          aria-label="Odegaard Writing and Research Center"
        >Odegaard Writing and Research Center</a>
      </li>
      <li>
        <a
          href="http://aep.washington.edu/"
          target="_blank"
          aria-label="Academic English Program"
        >Academic English Program</a>
      </li>
    </ul>

    <h4 class="h5 myuw-card-header">
      Social Events
    </h4>
    <ul class="list-unstyled">
      <li>
        <a
          href="http://www.fiuts.org/events"
          target="_blank"
          aria-label="FIUTS Event Calendar"
        >FIUTS Event Calendar</a>
      </li>
    </ul>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  computed: mapState({
    user: (state) => state.user,
  }),
};
</script>
