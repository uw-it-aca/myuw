<template>
  <div>
    <div :class="`w-100 myuw-border-top border-c${section.color_id}`" />
    <uw-card loaded>
      <template #card-heading>
        <div class="d-flex justify-content-between">
          <div>
            <h4>
              {{ section.curriculum_abbr }}
              {{ section.course_number }}
              {{ section.section_id }}
            </h4>
            <span>{{ section.course_title }}</span>
          </div>
          <div>
            <span class="d-block">
              {{ ucfirst(section.meetings[0].type) }}
            </span>
            <span
              v-if="section.is_primary_section && section.for_credit"
              class="d-block text-right"
            >
              {{ section.credits }} CR
            </span>
          </div>
        </div>
        <span v-if="section.summer_term">
          Summer
          {{
            section.summer_term
              .split('-')
              .map(ucfirst)
              .join('-')
          }}
        </span>
      </template>
      <template #card-body>
        <b-container fluid class="px-0">
          <b-row no-gutters>
            <b-col v-if="showRowHeading" cols="3">
              Meeting Time
            </b-col>
            <uw-meeting-info :meetings="section.meetings" />
          </b-row>
          <b-row no-gutters>
            <b-col v-if="showRowHeading" cols="3">
              Meeting Time
            </b-col>
            <uw-resources :section="section" :course="course" />
          </b-row>
        </b-container>
      </template>
      <template #card-disclosure>
        <b-collapse :id="`instructors-collapse-${index}`" v-model="isOpen">
          <uw-instructor-info v-if="instructors" :instructors="instructors" />
        </b-collapse>
      </template>
      <template #card-footer>
        <span v-if="instructors.length > 0">
          <b-button
            v-if="!isOpen"
            v-b-toggle="`instructors-collapse-${index}`"
            variant="link"
            size="sm"
            class="w-100 p-0 border-0 text-dark"
          >
            SHOW INSTRUCTORS
          </b-button>
          <b-button
            v-else
            v-b-toggle="`instructors-collapse-${index}`"
            variant="link"
            size="sm"
            class="w-100 p-0 border-0 text-dark"
          >
            HIDE INSTRUCTORS
          </b-button>
        </span>
        <span v-else>
          No instructor information available
        </span>
      </template>
    </uw-card>
  </div>
</template>

<script>
import Card from '../../_templates/card.vue';
import MeetingInfo from './meeting-info.vue';
import Resources from './resources.vue';
import InstructorInfo from './instructor-info.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-meeting-info': MeetingInfo,
    'uw-resources': Resources,
    'uw-instructor-info': InstructorInfo,
  },
  props: {
    course: {
      type: Object,
      required: true,
    },
    section: {
      type: Object,
      required: true,
    },
    showRowHeading: {
      type: Boolean,
      default: false,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    instructors() {
      const seenUWRegId = new Set();
      return this.section.meetings
          .map((s) => s.instructors || [])
          .flat()
          .filter((i) => {
            if (seenUWRegId.has(i.uwregid)) return false;
            seenUWRegId.add(i.uwregid);
            return true;
          })
          .sort((i1, i2) => {
            if (i1.surname < i2.surname) return -1;
            if (i1.surname > i2.surname) return 1;
            return 0;
          });
    },
  },
};
</script>

