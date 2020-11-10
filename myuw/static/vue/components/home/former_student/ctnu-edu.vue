<template>
  <uw-card
    v-if="showCard"
    :loaded="true"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Professional and Continuing Education (PCE)
      </h3>
    </template>
    <template #card-body>
      <p>
        Whether you want to update your skills or delve into a new field,
        UW Professional &amp; Continuing Education can help.
      </p>
      <p><a href="https://www.pce.uw.edu" target="_blank" data-linklabel="PCE Info">About PCE</a></p>
      <h4 class="myuw-card-heading">
        Available programs
      </h4>
      <ul class="unstyled-list">
        <li><a href="https://www.pce.uw.edu/career-accelerator-certificates" target="_blank" data-linklabel="PCE Career Accelerator Programs">Career Accelerator Certificate Programs</a></li>
        <li><a href="https://www.pce.uw.edu/certificates" target="_blank" data-linklabel="PCE Certificate Programs">Certificate Programs</a></li>
        <li><a href="https://www.pce.uw.edu/degrees" target="_blank" data-linklabel="PCE Degree Programs">Degree Programs</a></li>
        <li><a href="https://www.pce.uw.edu/courses" target="_blank" data-linklabel="PCE Courses">Courses</a></li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      showCard: (state) => state.user.affiliations.no_1st_class_affi,
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
