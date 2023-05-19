<template>
  <uw-card-property :title="`Instructor${instructorCount > 1 ? 's' : ''} of Record`">
    <ul class="list-unstyled mb-0">
      <li v-for="(instructor, i) in section.instructors" :key="i" class="mb-1">
        {{ titleCaseName(instructor.display_name) }}
      </li>
    </ul>
    <div>
      <span class="myuw-text-sm fst-italic"
        >Only instructors of record have access to this course in MyUW and GradePage.
      </span>
      <uw-collapsed-item :part="submitGradesLearnMore" caller-id="InstructorsOfRecord">
        <template #collapsed-body>
          To add or remove an instructor of record, contact your departmental time schedule
          coordinator.
        </template>
      </uw-collapsed-item>
    </div>
  </uw-card-property>
</template>

<script>
import CardProperty from '../../../_templates/card-property.vue';
import CollapsedItem from '../../../_common/collapsed-part.vue';

export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-collapsed-item': CollapsedItem,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    instructorCount() {
      if (this.section.instructors) {
        return this.section.instructors.length;
      }
      return 0;
    },
    submitGradesLearnMore() {
      return {
        title: 'Learn more',
        id: 'submitGradesLearnMore' + this.section.sln,
      };
    },
  },
};
</script>
