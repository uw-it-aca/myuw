<template>
  <uw-card-property-group>
    <uw-card-property title="Course Stats">
      <ul class="mb-0 list-unstyled">
        <li v-if="'failure_rate' in section" class="mb-1">
          {{ (section.failure_rate * 100).toFixed(0) }}% historic course fail rate
        </li>
        <li class="mb-1">
          <a
            :href="`https://coda.uw.edu/#${section.year}-${
              section.quarter}-${section.curriculum_abbr}-${section.course_number
            }-${section.section_id}`"
            :title="`Course Dashboard for ${section.label}`"
          >
            View course statistics dashboard
          </a>
        </li>
      </ul>
    </uw-card-property>
  </uw-card-property-group>
</template>

<script>
import CardPropertyGroup from '../../_templates/card-property-group.vue';
import CardProperty from '../../_templates/card-property.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-card-property': CardProperty,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
};
</script>
