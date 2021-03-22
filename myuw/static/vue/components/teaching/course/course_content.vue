<template>
  <uw-card
    :id="idForSection(section)"
    v-meta="{term: term, course: section.anchor}"
    loaded
    :ribbon="{
      side: 'top',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :section="section" />
      <uw-joint-section :section="section" :parent-id="idForSection(section)" />
    </template>

    <template #card-body>
      <uw-meeting-info show-row-heading :section="section" />
      <uw-final-exam show-row-heading :section="section" />
      <uw-class-list show-row-heading :section="section" />
      <uw-stats show-row-heading :section="section" />
      <uw-materials show-row-heading :section="section"/>
      <uw-grading v-if="section.for_credit" show-row-heading :section="section"/>
      <uw-evaluation show-row-heading :section="section"/>
    </template>
    <template v-if="linkedSections.length > 0" #card-disclosure>
      <b-collapse
        :id="`secondary-${section.section_label}`"
        v-model="isOpen"
        @show="logDisclosureOpen"
      >
        <uw-linked-section
          v-for="(linkedSection, i) in linkedSections"
          :key="`secondary-${section.section_label}-${i}`"
          :section="linkedSection"
        />
      </b-collapse>
    </template>
    <template v-if="linkedSections.length > 0" #card-footer>
      <b-button
        v-b-toggle="`secondary-${section.section_label}`"
        variant="link"
        size="sm"
        class="w-100 p-0 border-0 text-dark"
      >
        <font-awesome-icon v-if="!isOpen" :icon="faCaretRight" />
        <font-awesome-icon v-else :icon="faCaretUp" />
        Secondary Sections ({{linkedSections.length}})
      </b-button>
    </template>
  </uw-card>
</template>

<script>
import {
  faThumbtack,
  faCaretRight,
  faCaretUp,
} from '@fortawesome/free-solid-svg-icons';

import Card from '../../_templates/card.vue';
import CourseHeader from '../../_common/course/inst/header.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';
import JointSection from './joint-section.vue';
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
    'uw-course-header': CourseHeader,
    'uw-joint-section': JointSection,
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
      faCaretRight,
      faCaretUp,
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
  methods: {
    logDisclosureOpen() {
      this.$logger.disclosureOpen(this);
    },
  }
};
</script>
