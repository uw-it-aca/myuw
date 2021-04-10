<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <div class="d-flex">
      <div class="w-25 flex-fill">
        <div :class="`c${section.color_id} simplesquare`" />
        <h3 class="h6 myuw-font-encode-sans text-nowrap"
          :aria-label="section.id.replace(/-/g,' ')">
          <a
            v-inner="'View inst course card'"
            :href="`/teaching/${section.href}`"
            :future-nav-target="section.navtarget"
            title="Click to view the card on Teaching page"
          >
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
          </a>
        </h3>
        <div>
          <h4 class="sr-only">
            Section Type:
          </h4>
          <span class="text-capitalize">
            {{ section.section_type }}
          </span>
        </div>
        <div v-if="section.sln">
          <h4 class="sr-only">
            Section SLN:
          </h4>
          <a
            v-out="'Time Schedule for SLN'"
            :href="getTimeScheHref(section)"
            :title="`Time Schedule for SLN ${section.sln}`"
          >
            {{ section.sln }}
          </a>
        </div>
      </div>

      <div class="w-60 flex-fill">
        <h4 class="sr-only">
          Section Meetings:
        </h4>
        <uw-meeting-info :section="section" />
      </div>

      <div class="w-15 ml-3 flex-fill">
          <h4 class="sr-only">
            Section Enrollments:
          </h4>
          <uw-enrollment :section="section" />
      </div>
    </div>

    <template v-if="getLinkedSections(section).length > 0">
      <b-button
        v-b-toggle="`linked-sections-${section.id}`"
        variant="light" block
        class="p-0 text-dark"
      >
        Linked Sections of {{ section.curriculum_abbr }}
        {{ section.course_number }} {{ section.section_id }}
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" />
        <font-awesome-icon v-else :icon="faChevronUp" />
      </b-button>

      <b-collapse :id="`linked-sections-${section.id}`" v-model="isOpen">
        <uw-linked-section
          v-for="(sec, j) in getLinkedSections(section)"
          :key="`secondary-${section.id}-${j}`"
          :section="sec"
        />
      </b-collapse>
    </template>
    <hr>
  </div>
</template>

<script>
import {
  faThumbtack,
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';
import LinkedSection from '../../_common/course/inst/linked-section.vue';
import Enrollment from '../../_common/course/inst/enrollment.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';

export default {
  components: {
    'uw-linked-section': LinkedSection,
    'uw-meeting-info': MeetingInfo,
    'uw-enrollment': Enrollment,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
      faThumbtack,
      faChevronUp,
      faChevronDown,
    };
  },
  methods: {
    getLinkedSections(pSection) {
      return this.$parent.sections.filter(
        (section) => (!section.is_primary_section &&
          section.primary_section_label === pSection.section_label),
      );
    },
  },
};
</script>
