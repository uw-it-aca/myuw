<template>
  <ul class="list-unstyled">
    <li
      v-for="section in sections"
      :key="section.course_number"
      class="mb-2"
    >
      <div class="d-flex align-content-center">
        <div class="w-50">
          <font-awesome-icon
            :icon="faSquareFull"
            :class="`text-c${section.color_id}`"
            class="me-1"
          />
          <span class="h6 myuw-font-encode-sans m-0">
            {{ section.curriculum_abbr }} {{ section.course_number }}
          </span>
        </div>
        <div class="w-50 text-end text-nowrap">
          <span
            v-if="section.grade === 'X'"
            class="m-0 me-2 text-muted fst-italic myuw-text-md"
          >
            No grade yet
          </span>
          <span class="h6 myuw-font-encode-sans m-0">
            {{ section.grade }}
          </span>
        </div>
      </div>
    </li>
  </ul>
</template>

<script>
import {
  faSquareFull,
} from '@fortawesome/free-solid-svg-icons';

export default {
  props: {
    sections: {
      type: Array,
      default: false,
    },
  },
  data: function() {
    return {
      faSquareFull,
    };
  },
};
</script>
