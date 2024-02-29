<template>
  <uw-card
    v-if="internationalStudent && (!isReady || notices.length > 0)"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        International Student Check-In & Welcome
      </h2>
    </template>
    <template v-if="!isErrored" #card-body>
      <h3 class="h6 myuw-font-encode-sans">Immigration Check-In with International Student Services
      </h3>
      <div class="myuw-text-md mb-3">
        Complete the <a href="https://isss.uw.edu/">Immigration Check-In</a> once you have arrived
        in the U.S. It is an easy, online form that allows the UW to notify the U.S. government as
        required under federal regulations that you have arrived and reported to the ISS. Review
        the <a href="https://iss.washington.edu/post-arrival-checklist/">Post-Arrival Checklist</a>
         and follow the steps to complete this requirement before the first day of class.
      </div>

      <h3 class="h6 myuw-font-encode-sans">Virtual International Husky Welcome</h3>
      <div class="myuw-text-md mb-2">
        The Center for International Relations and Cultural Leadership Exchange (CIRCLE), invites
        you to the
        <a href="https://www.washington.edu/circle/new-students/international-husky-welcome/">2024
          Virtual International Husky Welcome!</a> Sign up for one of nine Zoom sessions
        on June 15 or June 22. Together, we will guide you through the first steps of college,
        introduce you to campus resources, and help you get ready for your Advising & Orientation
        sessions.
      </div>

<!-- USED FOR SWS Notice NSF001000 – Awaiting updates & implementation
      <div
        v-for="notice in notices"
        :key="notice.id_hash"
        class="myuw-text-md mb-2"
        v-html="notice.notice_body"
      />
-->
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      internationalStudent: (state) => state.user.affiliations.intl_stud,
      notices: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_fiuts'),
        );
      },
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
  },
  created() {
    if (this.internationalStudent) this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>
