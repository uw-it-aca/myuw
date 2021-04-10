<template>
  <div class="d-flex">
    <h3 class="w-25 myuw-text-md myuw-font-encode-sans"
      :class="{'sr-only': showRowHeader}">
      Course Stats
    </h3>
    <ul class="w-75">
      <li v-if="section.failure_rate">
        {{ (section.failure_rate * 100).toFixed(0) }}% historic course fail rate
      </li>
      <li>
        <a
          :href="`https://coda.uw.edu/#${section.year}-${
            section.quarter}-${section.curriculum_abbr}-${section.course_number
          }-${section.section_id}`"
          :title="`Course Dashboard for ${section.label}`"
        >
          View course stats
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    showRowHeader: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
