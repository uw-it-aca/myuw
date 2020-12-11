<template>
  <div id="classlist_table_view"
       aria-labelledby="table-view"
  >
    <h4 class="sr-only">
      Table of Student Information
    </h4>
    <div class="">
      <table id="student-list" class="">
        <thead>
          <tr>
            <th id="student-number">
              Student No.
            </th>
            <th id="uwnetid">
              UW NetID
            </th>
            <th id="last-name">
              Last Name
            </th>
            <th id="first-name">
              First Name
            </th>
            <th v-if="section.has_joint" id="joint-section" class="">
              Joint Course
            </th>
            <th v-if="section.has_linked_sections" id="linked-section">
              Secondary Section
            </th>
            <th id="credits">
              Credits
            </th>
            <th id="class-level">
              Class
            </th>
            <th id="majors">
              Majors
            </th>
            <th v-if="section.is_independent_start" id="start-date">
              Start Date
            </th>
            <th v-if="section.is_independent_start" id="end-date">
              End Date
            </th>
            <th id="email">
              <span class="sr-only">Email</span>
            </th>
          </tr>
        </thead>
        <tbody id="student-sort">
          <tr v-for="(reg, i) in section.registrations"
              :id="`student-${reg.regid}`"
              :key="i"
              :class="getClass(reg)"
          >
            <td headers="student-number">
              {{ reg.student_number }}
            </td>
            <td headers="uwnetid">
              {{ reg.netid }}
            </td>
            <td headers="last-name">
              {{ reg.surname }}
            </td>
            <td headers="first-name">
              {{ reg.first_name }}
            </td>
            <td v-if="section.has_joint"
                headers="joint-section"
                class="joint-col"
            >
              <span v-if="reg.is_joint">
                {{ reg.joint_curric }}
                {{ reg.joint_course_number }}
                {{ reg.joint_section_id }}
              </span>
              <span v-else>
                {{ section.curriculum_abbr }}
                {{ section.course_number }}
                {{ section.section_id }}
              </span>
            </td>
            <td v-if="section.has_linked_sections"
                headers="linked-section"
            >
              {{ reg.linked_sections }}
            </td>
            <td headers="credits">
              <span v-if="reg.is_auditor">Audit</span>
              <span v-else>{{ reg.credits }}</span>
            </td>
            <td headers="class-level">
              {{ ucfirst(reg.class_level) }}
            </td>
            <td headers="majors">
              <div v-for="(major, j) in reg.majors" :key="j">
                <span v-if="major.name">
                  {{ ucfirst(major.name) }}
                </span>
                <span v-if="(j < reg.majors.length - 1)">
                  ,&nbsp;
                </span>
              </div>
            </td>
            <td v-if="section.is_independent_start"
                headers="start-date"
            >
              {{ reg.start_date }}
            </td>
            <td v-if="section.is_independent_start"
                headers="end-date"
            >
              {{ reg.end_date }}
            </td>
            <td headers="email">
              <a href="`mailto:${reg.email}`"
                 title="`Email ${reg.first_name} ${reg.surname}`"
              >
                <i class="fa fa-envelope-o" />
                <span class="sr-only">{{ reg.email }}</span>
              </a>
            </td>
          </tr>
        </tbody>
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
  methods: {
    getClass(reg) {
      return reg.is_joint ? 'joint' : '';
    },
  },
};
</script>
