<template>
  <uw-card-property title="Final Exam">
    <template v-if="section.final_exam">
      <template v-if="section.final_exam.no_exam_or_nontraditional">
        No Exam or Non-Traditional
      </template>
      <template v-else-if="section.final_exam.start_date">
        <p v-if="!section.is_primary_section" class="mb-0">
          The final exam for the primary section is:
        </p>
        <table
          class="mb-0 w-100 table table-sm table-borderless myuw-text-md"
        >
          <thead class="sr-only">
            <tr>
              <th :id="`final-days-${section.id}`">Day</th>
              <th :id="`final-time-${section.id}`">Time</th>
              <th :id="`final-location-${section.id}`">Location</th>
            </tr>
          </thead>
          <tbody>
            <td :headers="`final-days-${section.id}`">
              {{ section.final_exam.start_date.format('ddd, MMM D') }}
            </td>
            <td :headers="`final-time-${section.id}`"
              class="p-0 text-left text-nowrap">
              {{ section.final_exam.start_date.format('h:mm') }} &ndash;
              {{ section.final_exam.end_date.format('h:mm A') }}
            </td>
            <td :headers="`final-location-${section.id}`" class="p-0 text-center">
              <uw-meeting-location :meeting="section.final_exam" />
            </td>
          </tbody>
        </table>
      </template>
      <template v-else-if="displayNoFinalPeriod">
        No final exam period during summer quarter.
      </template>
      <template v-else>
        Day and time to be arranged.
      </template>
    </template>
    <template v-else>
      No Final Exam Scheduled.
    </template>
    <a
      v-if="displayConfirmFinalLink"
      :href="confirmFinalLink"
    >
      Confirm final exam
    </a>
  </uw-card-property>
</template>

<script>
import Location from '../../_common/course/meeting/location.vue';
import CardProperty from '../../_templates/card-property.vue';

export default {
  components: {
    'uw-card-property': CardProperty,
    'uw-meeting-location': Location,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      displayConfirmFinalLink: false,
      displayNoFinalPeriod: false,
    };
  },
  computed: {
    confirmFinalLink() {
      return ''.concat(
        'https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/finalexam.aspx?quarter=',
        this.titleCaseWord(this.section.quarter), '+', this.section.year, '+',
        this.section.year, '&sln=', this.section.sln, '&chanid=');
    }
  },
  mounted() {
    if (
      this.section.is_primary_section &&
      this.section.final_exam &&
      !this.section.final_exam.no_exam_or_nontraditional &&
      !this.section.final_exam.is_confirmed &&
      this.section.sln
    ) {
      if (this.section.quarter.toLowerCase() === 'summer') {
        this.displayNoFinalPeriod = true;
      } else {
        this.displayConfirmFinalLink = true;
      }
    }
  },
};
</script>

<style lang="scss" scoped>
.table-sm {
  td {
    width: 33%;
    padding: 0;
  }
}
</style>