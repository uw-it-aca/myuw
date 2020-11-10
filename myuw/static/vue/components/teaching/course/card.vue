<template>
  <uw-card
    loaded
    :ribbon="{
      side: section.is_primary_section ? 'top' : 'left',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :section="section" />
      <div v-if="section.summer_term">
        Summer {{ section.summer_term.split('-').map(ucfirst).join('-') }}
      </div>
      <div v-if="section.cc_display_dates">
        Dates: {{ sectionFormattedDates(section) }}
      </div>
      <div v-if="section.on_standby">
        Your status: On Standby
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseHeader from '../../_common/course/header.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-header': CourseHeader,
  },
  props: {
    schedule: {
      type: Object,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
  },
  methods: {
  },
}
</script>

<style lang="scss" scoped>
.myuw-ribbon-top {
  height: 0.5rem;
  width: 100%;
}
.myuw-ribbon-left {
  width: 0.5rem;
}
</style>