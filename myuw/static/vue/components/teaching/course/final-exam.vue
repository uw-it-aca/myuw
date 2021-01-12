<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Final Exam
    </h5>
    <div v-if="section.final_exam">
      <div v-if="section.final_exam.no_exam_or_nontraditional">
        No Exam or Non-Traditional
      </div>
      <div v-else-if="section.final_exam.start_date">
        <p v-if="!section.is_primary_section">
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
              class="p-0 text-center text-nowrap">
              {{ section.final_exam.start_date.format('h:mm A') }} &ndash;
              {{ section.final_exam.end_date.format('h:mm A') }}
            </td>
            <td :headers="`final-location-${section.id}`" class="p-0 text-right">
              <span v-if="section.final_exam.is_remote">
                Remote
              </span>
              <span v-else>
                <span v-if="section.final_exam.building">
                  <a v-if="section.final_exam.latitude"
                    :href="locationUrl(section.final_exam)"
                    target="_blank"
                    :title="`Map of ${section.final_exam.building}`"
                  >
                    {{ section.final_exam.building }}
                  </a>
                  <span v-else title="No building information available">
                    {{ section.final_exam.building }}
                  </span>
                </span>

                <span v-if="section.final_exam.room">
                  <a
                    v-if="section.final_exam.classroom_info_url"
                    :href="section.final_exam.classroom_info_url"
                    target="_blank"
                    title="View classroom information"
                  >
                    {{ section.final_exam.room }}
                  </a>
                  <span v-else title="No classroom information available">
                    {{ section.final_exam.room }}
                  </span>
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
      if (this.section.quarter.toLowerCase() === 'summer') {
        this.displayNoFinalPeriod = true;
      } else {
        this.displayConfirmFinalLink = true;
        this.confirmFinalLink = `https://sdb.admin.uw.edu/sisMyUWClass/uwnetid/pop/finalexam.aspx?quarter=${this.ucfirst(this.section.quarter)}+${this.section.year}&sln=${this.section.sln}&chanid=`;
      }
    }
  },
};
</script>
