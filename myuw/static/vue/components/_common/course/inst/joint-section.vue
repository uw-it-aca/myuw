<template>
  <div v-if="section.joint_sections && section.joint_sections.length"
    class="mt-0 mb-4 myuw-text-sm text-muted">
    Offered jointly with
    <span v-for="(jointSec, i) in section.joint_sections" :key="i">
      <span v-if="jointSec.is_ior">
        <a :href="`#${anchorId(jointSec)}`">
          {{ jointSec.course_abbr }}
          {{ jointSec.course_number }}
          {{ jointSec.section_id }}
        </a>
      </span>
      <span v-else>
        <span :id="`${parentId}-${anchorId(jointSec)}`">
          {{ jointSec.course_abbr }}
          {{ jointSec.course_number }}
          {{ jointSec.section_id }}
          <font-awesome-icon :icon="faExclamationTriangle" class="mr-1" />
        </span>
        <b-tooltip :target="`${parentId}-${anchorId(jointSec)}`">
          You are not an instructor of record for
          {{ jointSec.course_abbr }}
          {{ jointSec.course_number }}
          {{ jointSec.section_id }}.
          Contact your Time Schedule Coordinator and ask to be added as an
          instructor of record.
        </b-tooltip>
      </span>
      <span v-if="i != (section.joint_sections.length - 1)">, </span>
    </span>
  </div>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    section: {
      type: Object,
      required: true,
    },
    parentId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      faExclamationTriangle,
    };
  },
  methods: {
    anchorId(section) {
      return `${section.course_abbr_slug}-${section.course_number}-${section.section_id}`;
    },
  },
};
</script>
