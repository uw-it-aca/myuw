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

    <div>
      <button
        v-if="!section.mini_card"
        type="button"
        :value="`/teaching/${section.href}`"
        :aria-label="`Pin ${section.id} mini-card to teaching page`"
        title="Pin a mini-card onto teaching page"
      >
        Pin to teaching page
      </button>
      <button
        v-else
        type="button"
        :value="`/teaching/${section.href}`"
        :aria-label="`Remove ${section.id} mini-card from teaching page`"
        title="Remove the mini-card from teaching page"
      >
        Unpin
      </button>
    </div>
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
