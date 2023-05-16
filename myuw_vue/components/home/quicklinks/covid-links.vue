<template>
  <div class="mx-n3 mb-3 p-3 myuw-covid-links">
    <div v-if="instructor">
      <p class="myuw-text-sm">
        Zoom now has a permanent spot in the Quick Links above.
        You can add other links by customizing your Quick Links,
        including adding recently visited links from below.
      </p>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
export default {
  computed: {
    ...mapState({
      student: (state) => state.user.affiliations.student,
      instructor: (state) => state.user.affiliations.instructor,
      seattleStudent: (state) => state.user.affiliations.seattle,
      bothellStudent: (state) => state.user.affiliations.bothell,
      tacomaStudent: (state) => state.user.affiliations.tacoma,
      seattleEmp: (state) => state.user.affiliations.official_seattle,
      bothellEmp: (state) => state.user.affiliations.official_bothell,
      tacomaEmp: (state) => state.user.affiliations.official_tacoma,
    }),
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import '../../../../myuw/static/css/myuw/variables.scss';

.myuw-covid-links {
  background-color: lighten(map.get($theme-colors, "beige"), 10%) !important;
}

</style>
