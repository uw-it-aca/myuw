<template>
  <div id="classlist_table_view"
       aria-labelledby="table-view"
  >
    <h3 class="sr-only">
      Table of Student Information
    </h3>
    <div class="">
      <b-table
        id="student-list"
        hover
        show-empty
        sort-icon-left
        responsive
        head-variant="light"
        :fields="fields"
        :items="items"
        primary-key="netid"
      >
        <template #cell(email)="data">
          <a
            v-inner="'Email student'"
            :href="data.value.href"
            :title="data.value.title">
            <font-awesome-icon :icon="faEnvelope"/>
            <span class="sr-only">{{ data.value.email }}</span>
          </a>
        </template>
      </b-table>
    </div>
  </div>
</template>
<script>
import {
  faEnvelope,
} from '@fortawesome/free-solid-svg-icons';
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
    showJointCourseStud: {
      type: Boolean,
      required: true,
    },
  },
  data: function() {
    return {
      faEnvelope,
    };
  },
  computed: {
    fields() {
      const data = [
        {
          key: 'studentNumber',
          label: 'Student No.',
        },
        {
          key: 'netid',
          label: 'UW NetID',
          sortable: true,
        },
        {
          key: 'surName',
          label: 'Last Name',
          sortable: true,
        },
        {
          key: 'Pronouns',
          label: 'Pronouns',
          sortable: true,
        },
        {
          key: 'firstName',
          label: 'First Name',
          sortable: true,
        },
      ];
      if (this.showJointCourseStud) {
        data.push(
            {
              key: 'jointCourse',
              label: 'Joint Course',
            },
        );
      }
      if (this.section.has_linked_sections) {
        data.push(
            {
              key: 'linkedSection',
              label: 'Linked Section',
              sortable: true,
            },
        );
      }
      data.push(
          {
            key: 'credits',
            label: 'Credits',
            sortable: true,
          },
          {
            key: 'classLevel',
            label: 'Class',
            sortable: true,
          },
          {
            key: 'majors',
            label: 'Majors',
          },
      );
      if (this.section.is_independent_start) {
        data.push(
            {
              key: 'startDate',
              label: 'Start Date',
            },
            {
              key: 'endDate',
              label: 'End Date',
            },
        );
      }
      data.push(
          {
            // class: "sr-only",
            key: 'email',
            label: 'Email',
          },
      );
      return data;
    },
    items() {
      const data = [];
      for (let i = 0; i < this.section.registrations.length; i++) {
        const reg = this.section.registrations[i];
        if (reg.isJoint && !this.showJointCourseStud) {
          continue;
        }
        const dataItem = {
          studentNumber: reg.student_number,
          netid: reg.netid,
          surName: reg.surname,
          firstName: reg.first_name,
          Pronouns: reg.pronouns,
        };
        if (this.showJointCourseStud) {
          dataItem.jointCourse = (
            reg.isJoint ?
            (reg.jointCurric + ' ' + reg.jointCourseNumber+ ' ' + reg.jointSectionId) :
            (this.section.curriculum_abbr + ' ' + this.section.course_number + ' ' +
            this.section.section_id));
        }
        if (this.section.has_linked_sections) {
          dataItem.linkedSection = reg.linked_sections;
        }
        dataItem.credits = reg.is_auditor ? 'Audit' : reg.credits;
        dataItem.classLevel = this.titleCaseWord(reg.class_level);
        dataItem.majors = this.combineMajors(reg.majors);
        if (this.section.is_independent_start) {
          dataItem.startDate = reg.start_date;
          dataItem.endDate = reg.end_date;
        }
        dataItem.email = {
          email: reg.email,
          href: 'mailto:' + reg.email,
          title: 'Email ' + reg.first_name + ' ' + reg.surname,
        };
        data.push(dataItem);
      }
      return data;
    },
  },
};
</script>
