<template>
  <div>
    <div class="d-flex">
      <uw-course-title show-sln :section="section" class="flex-fill" />

      <button v-if="section.mini_card"
        type="button"
        :title="`Remove mini-card of ${section.label}`"
        class="btn btn-link btn-sm ms-3 align-self-start p-0"
        @click="toggleMiniWrapper"
      >
        <font-awesome-icon :icon="faTimes" />
      </button>
    </div>

    <uw-joint-section :section="section" :parent-id="section.anchor" />

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
import JointSection from './joint-section.vue';
import CourseTitle from '../course-title.vue';
import CardProperty from '../../../_templates/card-property.vue';

export default {
  components: {
    'uw-course-title': CourseTitle,
    'uw-card-property': CardProperty,
    'uw-joint-section': JointSection,
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
