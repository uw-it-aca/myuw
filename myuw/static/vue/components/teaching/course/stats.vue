<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Course Stats
    </h5>
    <ul>
      <li v-if="section.failure_rate">
        {{ (section.failure_rate * 100).toFixed(0) }}% historic course fail rate
      </li>
      <li>
        <a
          v-out="`Course Dashboard ${section.id}`"
          :href="`https://coda.uw.edu/#${section.year}-${
            section.quarter}-${section.curriculum_abbr}-${section.course_number
          }-${section.section_id}`"
          :title="`Course Dashboard for ${section.id}`"
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
