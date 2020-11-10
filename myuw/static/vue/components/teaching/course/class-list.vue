<template>
  <div>
    <h5 :class="{'sr-only': showRowHeader}">
      Enrollment
    </h5>
    <table class="mb-0 w-100 table table-sm table-borderless myuw-text-md">
      <thead class="sr-only">
        <tr>
          <th :id="`enrolled-${section.id}`">
            Enrolled
          </th>
          <th :id="`list-link-${section.id}`">
            Class List Link
          </th>
          <th :id="`list-csv-${section.id}`">
            Download Class List CSV
          </th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td :headers="`enrolled-${section.id}`">
            {{ section.current_enrollment }} of
            {{ section.limit_estimated_enrollment }}
          </td>
          <td :headers="`list-link-${section.id}`">
            <a :href="`/teaching/${section.year},${section.quarter},${
              section.curriculum_abbr},${section.course_number
            }/${section.section_id}/students`"
            >
              View class list
            </a>
          </td>
          <td :headers="`list-csv-${section.id}`">
            <a href="#">
              TODO: Download class list csv
            </a>
          </td>
        </tr>
      </tbody>
    </table>
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
