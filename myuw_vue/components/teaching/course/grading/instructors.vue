<template>
    <uw-card-property title="Instructors of Record">
      <ol>
        <li
          v-for="(instructor, i) in section.instructors" :key="i" class="mb-1">
            {{ titleCaseName(instructor.display_name) }}
        </li>
      </ol>
      <div>
        Only instructors of record can submit grades
        <uw-collapsed-item
          :notice="submitGradesLearnMore" caller-id="InstructorsOfRecord">
          <template #notice-body>
            To add or remove ...
          </template>
        </uw-collapsed-item>
      </div>
    </uw-card-property>
</template>

<script>
import CardProperty from '../../../_templates/card-property.vue';
import CollapsedItem from '../../../_common/collapsed-item.vue';

export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-collapsed-item': CollapsedItem
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {
    submitGradesLearnMore() {
      return {
        notice_title: "Learn more",
        id_hash: "submitGradesLearnMore" + this.section.sln,
      };
    },
  },
};
</script>
