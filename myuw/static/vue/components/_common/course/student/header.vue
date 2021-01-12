<template>
  <div>
    <div>
      <uw-course-title show-credits :section="section" />
    </div>

    <div v-if="section.summer_term" class="d-flex">
      <h5 class="sr-only">
        Term:
      </h5>
      <div class="myuw-text-md">
        Summer
        {{
          section.summer_term
            .split('-')
            .map(ucfirst)
            .join('-')
        }}
      </div>
    </div>

    <div v-if="section.cc_display_dates" class="d-flex">
      <h5
        class="w-25 myuw-text-md"
      >
        Dates:
      </h5>
      <div class="myuw-text-md">
        {{ sectionFormattedDates(section) }}
      </div>
    </div>

    <div v-if="section.on_standby" class="d-flex">
      <h5
        class="w-25 myuw-text-md"
      >
        Your Status:
      </h5>
      <div class="myuw-text-md">
        On Standby
      </div>
    </div>
  </div>
</template>

<script>
import {
  faTimes,
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';
import CourseTitle from '../header.vue';

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
  data() {
    return {
      faTimes,
    };
  },
  methods: {
    ...mapActions('inst_schedule', [
      'toggleMini',
    ]),
  },
};
</script>
