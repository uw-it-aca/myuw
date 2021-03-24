<template>
  <div>
    <div>
      <uw-course-title show-sln :section="section" />

      <div>
        <b-button v-if="section.mini_card"
          variant="dark" size="sm"
          :title="`Remove mini-card of ${section.label}`"
          @click="toggleMiniWrapper"
        >
          <font-awesome-icon :icon="faTimes" />
        </b-button>
      </div>
    </div>

    <div v-if="section.summer_term" class="d-flex">
      <h3
        class="w-25 font-weight-bold myuw-text-md"
      >
        Term
      </h3>
      <div class="flex-fill myuw-text-md">
        Summer {{ capitalizeString(section.summer_term) }}
      </div>
    </div>

    <div v-if="section.cc_display_dates" class="d-flex">
      <h3
        class="w-25 font-weight-bold myuw-text-md"
      >
        Dates
      </h3>
      <div class="flex-fill myuw-text-md">
        {{ sectionFormattedDates(section) }}
      </div>
    </div>
  </div>
</template>

<script>
import {
  faTimes,
} from '@fortawesome/free-solid-svg-icons';
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
  data() {
    return {
      faTimes,
    };
  },
  methods: {
    ...mapActions('inst_schedule', [
      'toggleMini',
    ]),
    toggleMiniWrapper() {
      this.$logger.cardUnPin(this, this.section.apiTag);
      this.toggleMini(this.section);
      window.history.replaceState({}, null, window.location.pathname);
    }
  },
};
</script>
