<template>
  <uw-card
    v-if="showCard"
    :loaded="true"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Professional and Continuing Education (PCE)
      </h2>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        Whether you want to update your skills or delve into a new field,
        UW Professional &amp; Continuing Education can help.
      </p>
      <p class="myuw-text-md">
        <a href="https://www.pce.uw.edu">About PCE</a>
      </p>
      <h3 class="mt-4 h6 text-dark-beige myuw-font-encode-sans">
        Available programs
      </h3>
      <ul class="list-unstyled myuw-text-md mb-2">
        <li class="mb-1">
          <a v-out="'PCE Certificate Programs'" href="https://www.pce.uw.edu/certificates"
           >Certificate Programs</a>
        </li>
        <li class="mb-1">
          <a v-out="'PCE Degree Programs'" href="https://www.pce.uw.edu/degrees"
           >Degree Programs</a>
        </li>
        <li class="mb-1">
          <a v-out="'PCE Courses'" href="https://www.pce.uw.edu/courses"
           >Courses</a>
        </li>
        <li>
          <a v-out="'Specializations'"
            href="https://www.pce.uw.edu/specializations">Specializations</a>
        </li>
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
