<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <h4>
      <div :class="`c${section.color_id} simplesquare`" />
      <a
        :href="`/teaching/${section.href}`"
        :future-nav-target="section.navtarget"
      >
        {{ section.curriculum_abbr }}
        <span class="text-nowrap">
          {{ section.course_number }}
          {{ section.section_id }}
        </span>
      </a>
    </h4>

    <div>
      <span>
        {{ section.section_type.toUpperCase() }}
      </span>
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
    </div>

    <uw-meeting
      :section="section"
      :mobile-only="mobileOnly"
    />

    <slot />
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
