<template>
  <div v-if="section.is_primary_section || !section.isLinkedSecondary">
    <h4>
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
          :data-linklabel="getTimeScheLinkLable(section)"
          target="_blank"
        >
          {{ section.sln }}
        </a>
      </span>
    </div>

    <div>
      <h5 class="sr-only">
        Section Meetings:
      </h5>
      <uw-meeting :section="section" :mobile-only="mobileOnly" />
    </div>

    <div>
      <h5 class="sr-only">
        Section Enrollments:
      </h5>
      <uw-enrollment :section="section" />
    </div>

    <slot />
    <!-- for linked secondary sections -->
  </div>
</template>

<script>
import MeetingInfo from '../../_common/course/inst/meeting.vue';
import Enrollment from '../../_common/course/inst/enrollment.vue';

export default {
  components: {
    'uw-meeting': MeetingInfo,
    'uw-enrollment': Enrollment,
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
