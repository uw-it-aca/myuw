<template>
  <div>
    <div class="d-flex">
      <uw-course-title show-sln :section="section" class="flex-fill" />

      <b-button v-if="section.mini_card"
        variant="dark" size="sm"
        :title="`Remove mini-card of ${section.label}`"
        @click="toggleMiniWrapper"
        class="ml-3 align-self-start"
      >
        <font-awesome-icon :icon="faTimes" />
      </b-button>
    </div>

    <uw-card-property v-if="section.summer_term" title="Summer Term">
      {{ capitalizeString(section.summer_term) }}
    </uw-card-property>

    <uw-card-property v-if="section.cc_display_dates" title="Dates">
      {{ sectionFormattedDates(section) }}
    </uw-card-property>
  </div>
</template>

<script>
import {
  faTimes,
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';
import CourseTitle from '../course-title.vue';
import CardProperty from '../../../_templates/card-property.vue';

export default {
  components: {
    'uw-course-title': CourseTitle,
    'uw-card-property': CardProperty,
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
