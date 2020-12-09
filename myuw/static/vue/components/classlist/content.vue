<template>
  <div id="classlist_table_view"
       aria-labelledby="list_view"
       role="tabpanel" aria-hidden="false"
  >
    <h4 class="sr-only">
      Table of Student Information
    </h4>
    <div class="">
      <table id="student_list" class="">
        <thead>
          <tr>
            <th>Student No.</th>
            <th>UW NetID</th>
            <th>Last Name</th>
            <th>First Name</th>
            <th v-if="section.has_joint" class="">
              Joint Course
            </th>
            <th v-if="section.has_linked_sections">
              Secondary Section
            </th>
            <th>Credits</th>
            <th>Class</th>
            <th>Major</th>
            <th v-if="section.is_independent_start">
              Start Date
            </th>
            <th v-if="section.is_independent_start">
              End Date
            </th>
            <th><span class="sr-only">Email</span></th>
          </tr>
        </thead>
        <tbody id="student_sort" />
      </table>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
    section: {
      type: Object,
      required: true,
    },
  },
  computed: {

  },
};
</script>
