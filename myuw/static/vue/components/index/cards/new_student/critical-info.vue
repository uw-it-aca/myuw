<template>
  <uw-card v-if="!isReady || student && hasRegisterNotices"
    :loaded="isReady" :errored="isErrored">
    <template #card-heading>
      <h3>
        Update Critical Information
      </h3>
    </template>
    <template v-if="!isErrored" #card-body>
      <div v-for="notice in notices" :key="notice.id_hash">
        <div v-html="notice.notice_title" />
        <div v-html="notice.notice_body" />
      </div>
      <div class="notice-content">
        <span class="notice-title">Update Student Directory</span>
        <span class="non-notice-body-with-title">
          Critical information (e.g. financial aid information) goes to your
          addresses found in the Student Directory, so keep them up to date.
          You can check your directory information by clicking on your
          username in the MyUW header above and you can update it by
          following links provided there.
        </span>
      </div>
      <div v-if="!isResident" class="notice-content">
        <span class="notice-title">Non-Resident Classification</span>
        <span class="non-notice-body-with-title">
          You are currently classified as a "Non-Resident.”
          If you believe you qualify for
          <a
            href="http://www.washington.edu/students/reg/residency/index.html"
          >
            resident status
          </a>, you may apply for a change of status by completing the
          <a
            href="http://www.washington.edu/students/reg/residency/applicationProcess.html"
          >
            Residence Questionnaire
          </a>, or contact the Residency Office at
          <a href="mailto:resquest@uw.edu">
            resquest@uw.edu
          </a> or 206-543-5932.
        </span>
      </div>
    </template>
    <template v-else #card-body>
      <p class="text-danger">
        <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
        An error occurred and MyUW cannot load your notices right now. Please
        try again later.
      </p>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_email'),
        );
      },
      isResident: (state) => {
        let isResident = true;

        state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_residence'),
        )[0].attributes.forEach((attr) => {
          if (attr.name === 'ResidencyStatus' &&
              attr.value !== '1' &&
              attr.value !== '2') {
            isResident = false;
          }
        });

        return isResident;
      },
      student: (state) => state.user.affiliations.student,
    }),
    ...mapGetters('notices', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      hasRegisterNotices: 'hasRegisterNotices',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('notices', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
.notice-title, .notice-body-with-title, .non-notice-body-with-title {
  display: block;
}
</style>
