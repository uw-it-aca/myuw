<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <div  class="d-flex">
      <h4 class="">
        <div :class="`c${section.color_id} simplesquare`" />
        <a
          :href="`/teaching/${section.href}`"
          :future-nav-target="section.navtarget"
          title="Click to view the card on Teaching page"
        >
          {{ section.curriculum_abbr }}
          <span class="text-nowrap">
            {{ section.course_number }}
            {{ section.section_id }}
          </span>
        </a>
      </h4>
      <div>
        <div>
          <h5 class="sr-only">
            Section Type:
          </h5>
          <span class="text-capitalize">
            {{ section.section_type }}
          </span>
        </div>
        <div v-if="section.sln">
          <h5 class="sr-only">
            Section SLN:
          </h5>
          <span>
            <a
              :href="getTimeScheHref(section)"
              :title="`Time Schedule for SLN ${section.sln}`"
              v-out="getTimeScheLinkLable(section)"
              target="_blank"
            >
              {{ section.sln }}
            </a>
          </span>
        </div>
      </div>

      <div class="flex-fill">
        <h5 class="sr-only">
          Section Meetings:
        </h5>
        <uw-meeting-info :section="section" />
      </div>

      <div>
        <h5 class="sr-only">
          Section Enrollments:
        </h5>
        <uw-enrollment :section="section" />
      </div>
    </div>

    <template v-if="getLinkedSections(section).length > 0">
      <b-button
        v-b-toggle="`linked-sections-${section.id}`"
        variant="light" block
        class="p-0 text-dark"
        title="Show/Hide linked secondary sections"
      >
        <font-awesome-icon v-if="!isOpen" :icon="faCaretRight" />
        <font-awesome-icon v-else :icon="faCaretDown" />
        Linked Sections of {{ section.curriculum_abbr }}
        {{ section.course_number }} {{ section.section_id }}
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
  faCaretRight,
  faCaretDown,
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
      faCaretRight,
      faCaretDown,
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
