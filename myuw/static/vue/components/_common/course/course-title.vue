<template>
  <div class="d-flex justify-content-between mb-3">
    <div>
      <h4
        class="h5 mb-0 text-dark-beige myuw-font-encode-sans">
        {{ section.curriculum_abbr }}
        {{ section.course_number }}
        {{ section.section_id }}
      </h4>
      <div>{{ section.course_title }}</div>
    </div>

    <div class="d-flex">
      <span v-if="showSln && section.sln" class="mr-2">
        SLN
        <a
        v-out="getTimeScheLinkLable(section)"
        :href="getTimeScheHref(section)"
        :title="`Time Schedule for SLN ${section.sln}`"
        target="_blank"
        >
          {{ section.sln }}
        </a>
      </span>

      <div>
        <div :class="`px-1 border myuw-text-sm
        text-uppercase text-c${section.color_id}`"
        >
          {{ section.section_type }}
        </div>
      </div>

      <div v-if="showCredits && section.is_primary_section && section.for_credit"
          :class="`px-1 myuw-text-sm text-right
          text-uppercase text-c${section.color_id}`"
        >
          {{ section.credits }} CR
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    showSln: {
      type: Boolean,
      default: false,
    },
    showCredits: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
