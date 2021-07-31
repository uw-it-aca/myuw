<template>
  <uw-card
    :id="section.anchor"
    v-meta="{term: term, course: section.anchor}"
    loaded
    :ribbon="{
      side: 'top',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :section="section" />
    </template>

    <template #card-body>
      <uw-card-property-group>
        <uw-meeting-info show-row-heading :section="section" />
        <uw-final-exam :section="section" />
      </uw-card-property-group>
      <uw-class-list :section="section" />
      <uw-stats :section="section" />
      <uw-materials :section="section"/>
      <uw-grading v-if="section.for_credit" :section="section"/>
      <uw-evaluation v-if="section.evaluation" :section="section" />
    </template>
    <template v-if="linkedSections.length > 0" #card-disclosure>
      <b-collapse
        :id="`secondary-${section.section_label}`"
        v-model="isOpen"
      >
        <h3 class="myuw-text-md myuw-font-encode-sans pt-3">
            Linked Sections
        </h3>
        <uw-linked-section
          v-for="(linkedSection, i) in linkedSections"
          :key="`secondary-${section.section_label}-${i}`"
          :section="linkedSection"
        />
      </b-collapse>
    </template>
    <template v-if="linkedSections.length > 0" #card-footer>
      <button v-b-toggle="`secondary-${section.section_label}`"
        type="button"
        class="btn btn-link w-100 p-0 border-0 text-dark"
      >
        Linked Sections of {{ section.curriculum_abbr }}
        {{ section.course_number }} {{ section.section_id }}
        <font-awesome-icon v-if="!isOpen"  :icon="faChevronDown" />
        <font-awesome-icon v-else :icon="faChevronUp" />
      </button>
    </template>
  </uw-card>
</template>

<script>
import {
  faThumbtack,
  faChevronUp,
  faChevronDown,
} from '@fortawesome/free-solid-svg-icons';

import Card from '../../_templates/card.vue';
import CardPropertyGroup from '../../_templates/card-property-group.vue';
import CourseHeader from '../../_common/course/inst/header.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';
import FinalExam from './final-exam.vue';
import ClassList from './classlist.vue';
import Stats from './stats.vue';
import Materials from './materials.vue';
import Grading from './grading.vue';
import Evaluation from './evaluation.vue';
import LinkedSection from '../../_common/course/inst/linked-section.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property-group': CardPropertyGroup,
    'uw-course-header': CourseHeader,
    'uw-meeting-info': MeetingInfo,
    'uw-final-exam': FinalExam,
    'uw-class-list': ClassList,
    'uw-stats': Stats,
    'uw-materials': Materials,
    'uw-grading': Grading,
    'uw-evaluation': Evaluation,
    'uw-linked-section': LinkedSection,
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
  data() {
    return {
      isOpen: false,
      faThumbtack,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    linkedSections() {
      return this.schedule.sections.filter(
        (section) => section.primary_section_label === this.section.section_label
      );
    },
    term() {
      return this.section.year + "," + this.section.quarter;
    },
  },
  mounted() {
    const currentUrl = window.location.href;
    if (currentUrl.endsWith(this.section.anchor)) {
      this.selfAnchoredOnce(this.section);
    }
  },
};
</script>
