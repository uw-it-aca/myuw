<template>
  <uw-card
    :id="idForSection(section)"
    loaded
    :ribbon="{
      side: 'left',
      colorId: section.color_id,
    }"
  >
    <template #card-heading>
      <uw-course-header :section="section" />
      <uw-joint-section :section="section" :parent-id="idForSection(section)" />
    </template>
    <template #card-body>
      <uw-meeting-info show-row-heading :section="section" />
      <uw-class-list show-row-heading :section="section" />
      <uw-materials show-row-heading :section="section" />
    </template>
  </uw-card>
</template>

<script>
import Card from '../../_templates/card.vue';
import CourseHeader from '../../_common/course/header.vue';
import MeetingInfo from '../../_common/course/meeting-info.vue';
import JointSection from './joint-section.vue';
import ClassList from './class-list.vue';
import Materials from './materials.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-header': CourseHeader,
    'uw-joint-section': JointSection,
    'uw-meeting-info': MeetingInfo,
    'uw-class-list': ClassList,
    'uw-materials': Materials,
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
  mounted() {
    const currentUrl = window.location.href;
    if (currentUrl.endsWith(this.section.anchor)) {
      this.selfAnchored(this.section);
    }
  },
};
</script>
