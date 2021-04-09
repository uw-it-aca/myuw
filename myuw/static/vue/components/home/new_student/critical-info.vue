<template>
  <uw-card
    v-if="!isReady || student && hasRegisterNotices"
    :loaded="isReady" :errored="isErrored"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Update Critical Information
      </h2>
    </template>
    <template v-if="!isErrored" #card-body>
      <!-- notice template where data is inserted -->
      <div v-for="notice in notices" :key="notice.id_hash">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans"
          v-html="notice.notice_title" />
        <div class="mb-4 myuw-text-md" v-html="notice.notice_body" />
      </div>
      <!-- static notice content, goes after dynamic notices -->
      <div class="notice-content">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          <span class="notice-title">Update Student Directory</span>
        </h3>
        <div class="mb-4 myuw-text-md">
          <span class="non-notice-body-with-title">
            Critical information (e.g. financial aid information) goes to your
            addresses found in the Student Directory, so keep them up to date.
            You can check your directory information by clicking on your
            username in the MyUW header above and you can update it by
            following links provided there.
          </span>
        </div>
      </div>
      <div v-if="!isResident" class="notice-content">
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          <span class="notice-title">Non-Resident Classification</span>
        </h3>
        <div class="mb-4 myuw-text-md">
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
      notices: (state) => {
        return state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_email'),
        );
      },
      isResident: (state) => {
        let isResident = true;
        const notices = state.notices.value.filter(
            (notice) => notice.location_tags.includes('checklist_residence'),
        )[0];

        if (notices) {
          notices.attributes.forEach((attr) => {
            if (attr.name === 'ResidencyStatus' &&
                attr.value !== '1' &&
                attr.value !== '2') {
              isResident = false;
            }
          });
        }

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
