<template>
  <div>
    <div>
      <uw-course-title show-credits :section="section" />
    </div>

    <div v-if="section.summer_term">
      <h3 class="sr-only">
        Term:
      </h3>
      <div class="myuw-text-md">
        Summer {{ capitalizeString(section.summer_term) }}
      </div>
    </div>

    <div v-if="section.cc_display_dates" class="d-flex">
      <h3 class="mr-2 myuw-text-md">
        Dates:
      </h3>
      <div class="myuw-text-md">
        {{ sectionFormattedDates(section) }}
      </div>
    </div>

    <div v-if="section.on_standby" class="d-flex">
      <h3 class="mr-2 myuw-text-md">
        Your Status:
      </h3>
      <div class="myuw-text-md">
        On Standby
      </div>
    </div>
  </div>
</template>

<script>
import {mapActions} from 'vuex';
import CourseTitle from '../course-title.vue';

export default {
  components: {
    'uw-course-title': CourseTitle,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  methods: {
    ...mapActions('inst_schedule', [
      'toggleMini',
    ]),
  },
};
</script>
