<template>
  <uw-card
    :id="section.anchor"
    v-meta="{term: term, course: section.anchor}"
    loaded
    :ribbon="{
      side: 'left',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :section="section" />
    </template>

    <template #card-body>
      <uw-meeting-info show-row-heading :section="section" />
      <uw-class-list :section="section" />
      <uw-materials :section="section" />
      <uw-grading v-if="section.allows_secondary_grading" :section="section"/>
      <uw-evaluation v-if="section.evaluation && !section.evaluation.eval_not_exist"
        :section="section" />
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';
import CourseHeader from '../../_common/course/inst/header.vue';
import MeetingInfo from '../../_common/course/meeting/schedule.vue';
import ClassList from './classlist.vue';
import Materials from './materials.vue';
import Grading from './grading/grading.vue';
import Evaluation from './evaluation.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-header': CourseHeader,
    'uw-meeting-info': MeetingInfo,
    'uw-class-list': ClassList,
    'uw-materials': Materials,
    'uw-grading': Grading,
    'uw-evaluation': Evaluation,
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
    term() {
      return this.schedule.year + ',' + this.schedule.quarter;
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
