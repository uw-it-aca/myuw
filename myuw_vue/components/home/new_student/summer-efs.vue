<template>
  <uw-card
    v-if="showContent"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
    </template>

    <template #card-body>
      <div v-for="notice in notices" :key="notice.id_hash" class="mb-3">
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          Review Critical Summer Registration Info
        </h2>
        <div class="myuw-text-md" v-html="notice.notice_body" />
      </div>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Consider College Edge
      </h2>
      <div class="myuw-text-md mb-2">
        College Edge allows students to arrive early and start strong. This optional program
        invites incoming students to get acclimated to life at UW and complete a 5-credit course
        before Autumn Quarter begins. College Edge courses are intimate, experiential and apply to
        your UW degree. College Edge students can move into the UW Residence Halls in mid-August
        and have the option to stay put for the academic year.
        <a href="https://CollegeEdge.uw.edu">Learn more about College Edge.</a>
      </div>
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
      seattle: (state) => state.user.affiliations.seattle,  // fix/MUWM-5096
      notices: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('checklist_summerreg'),
        );
      },
      student: (state) => state.user.affiliations.student,
    }),
    ...mapGetters('notices', [
      'hasRegisterNotices',
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showContent() {
      return (this.student &&
        (!this.isReady || (this.seattle && this.hasRegisterNotices)));
    },
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student) this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>
