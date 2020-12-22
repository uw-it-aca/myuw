<template>
  <uw-card
    :id="idForSection(section)"
    loaded
    :ribbon="{
      side: section.is_primary_section ? 'top' : 'left',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :schedule="schedule" :section="section" />
      <uw-joint-section :section="section" :parent-id="idForSection(section)" />
    </template>
    <template #card-body>
      <uw-meeting-info show-row-heading :section="section" />
      <uw-final-exam show-row-heading :section="section" />
      <uw-class-list show-row-heading :section="section" />
      <uw-stats show-row-heading :section="section" />
      <uw-materials
        show-row-heading
        :section="section"
        :past-term="schedule.past_term"
      />
      <uw-grading show-row-heading :section="section"/>
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';
import CourseHeader from '../../_common/course/header.vue';
import MeetingInfo from '../../_common/course/meeting-info.vue';
import JointSection from './joint-section.vue';
import FinalExam from './final-exam.vue';
import ClassList from './class-list.vue';
import Stats from './stats.vue';
import Materials from './materials.vue';
import Grading from './grading.vue';

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
  },
};
</script>
