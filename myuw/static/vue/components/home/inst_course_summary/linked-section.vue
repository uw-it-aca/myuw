<template>
  <div>
    <!-- linked secondary section -->
    <div :class="`c${section.color_id}`" />
    <a
      :href="`/teaching/${section.href}`"
      :future-nav-target="`${section.navtarget}`"
    >
      {{ section.section_id }}
    </a>
    <span v-if="section.sln">
      <a
        :href="getTimeScheHref(section)"
        :title="`Time Schedule for SLN ${section.sln}`"
        :data-linklabel="getTimeScheLinkLable(section)"
        target="_blank"
      >
        {{ section.sln }}
      </a>
    </span>
    <span>
      {{ ucfirst(section.section_type) }}
    </span>

    <uw-meeting
      :section="section"
      :mobile-only="mobileOnly"
    />
  </div>
</template>

<script>
import MeetingInfo from './meeting.vue';

export default {
  components: {
    'uw-meeting': MeetingInfo,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>
