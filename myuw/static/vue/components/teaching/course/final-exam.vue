<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Final Exam
    </h5>
    <div v-if="section.final_exam">
      <span v-if="section.final_exam.no_exam_or_nontraditional">
        No Exam or Non-Traditional
      </span>
      <div v-else-if="section.final_exam.start_date">
        <div v-if="!section.is_primary_section">
          The final exam for the primary section is:
          <br>
        </div>
        <table
          v-else
          class="mb-0 w-100 table table-sm table-borderless myuw-text-md"
        >
          <thead class="sr-only">
            <tr>
              <th>Day</th>
              <th>Time</th>
              <th>Location</th>
            </tr>
          </thead>
          <tbody>
            <td>{{ section.final_exam.start_date.format('ddd, MMM D') }}</td>
            <td>
              {{ section.final_exam.start_date.format('hh:mm A') }}
              - {{ section.final_exam.end_date.format('hh:mm A') }}
            </td>
            <td>
              <span
                v-for="(locationData, i) in section.final_exam.locationData"
                :key="i"
              >
                <a
                  v-if="locationData.link"
                  :href="locationData.link"
                  :title="locationData.label"
                >
                  {{ locationData.text }}
                </a>
                <span v-else :title="locationData.label">
                  {{ locationData.text }}
                </span>
              </span>
            </td>
          </tbody>
        </table>
      </div>
      <div v-else-if="displayNoFinalPeriod">
        No final exam period during summer quarter.
      </div>
      <div v-else>
        Day and time to be arranged.
      </div>
    </div>
    <div v-else>
      No Final Exam Scheduled.
    </div>
    <a
      v-if="displayConfirmFinalLink"
      :href="confirmFinalLink"
      target="_blank"
      :label="`Confirm Final: ${section.curriculum_abbr} ${
        section.course_number} ${section.section_id}`"
    >
      Confirm final exam
    </a>
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
  data() {
    return {
      confirmFinalLink: null,
      displayConfirmFinalLink: false,
      displayNoFinalPeriod: false,
    };
  },
  mounted() {
    if (
      this.section.is_primary_section &&
      this.section.final_exam &&
      !this.section.final_exam.no_exam_or_nontraditional &&
      !this.section.final_exam.is_confirmed &&
      this.section.sln
    ) {
      if (this.section.quarter.toLowerCase() === 'Summer') {
        this.displayNoFinalPeriod = true;
      } else {
        this.displayConfirmFinalLink = true;
        this.confirmFinalLink = `https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/finalexam.aspx?quarter=${this.ucfirst(this.section.quarter)}+${this.section.year}&sln=${this.section.sln}&chanid=`;
      }
    }
  },
};
</script>
