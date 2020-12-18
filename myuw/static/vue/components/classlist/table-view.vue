<template>
  <div id="classlist_table_view"
       aria-labelledby="table-view"
  >
    <h4 class="sr-only">
      Table of Student Information
    </h4>
    <div class="">
      <b-table id="student-list"
               sort-icon-left hover head-variant="light" responsive="sm"
               :fields="fields" :items="items"
               primary-key="netid"
      >
        <template #cell(email)="data">
          <a :href="data.value.href" :title="data.value.title">
            <i class="fa fa-envelope-o" />
            <span class="sr-only">{{ data.value.email }}</span>
          </a>
        </template>
      </b-table>
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
    showJointCourseStud: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    fields() {
      let data = [
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
          key: 'firstName',
          label: 'First Name',
          sortable: true,
        },
      ];
      if (this. showJointCourseStud && this.section.has_joint) {
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
              label: 'Secondary Section',
              sortable: true,
            },
        );
      }
      data = data.concat([
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
        }],
      );
      if (this.section.is_independent_start) {
        data = data.concat([
          {
            key: 'startDate',
            label: 'Start Date',
          },
          {
            key: 'endDate',
            label: 'End Date',
          }],
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
        const dataItem = {
          studentNumber: reg.student_number,
          netid: reg.netid,
          surName: reg.surname,
          firstName: reg.first_name,
        };
        if (this.showJointCourseStud && this.section.has_joint) {
          dataItem.jointCourse = reg.is_joint ?
            (reg.joint_curric + ' ' + reg.joint_course_number + ' ' + reg.joint_section_id) :
            (this.section.curriculum_abbr + ' ' + this.section.course_number + ' ' +
            this.section.section_id);
        }
        if (this.section.has_linked_sections) {
          dataItem.linkedSection = reg.linked_sections;
        }
        dataItem.credits = reg.is_auditor ? 'Audit' : reg.credits;
        dataItem.classLevel = this.ucfirst(reg.class_level);
        if (reg.majors === undefined || reg.majors.length == 0) {
          dataItem.majors = '';
        } else {
          const majors = [];
          for (let j = 0; j < reg.majors.length; j++) {
            const mj = reg.majors[j];
            if (mj.name) {
              majors.push(this.ucfirst(mj.name));
            }
          }
          dataItem.majors = majors.length > 1 ? majors.join(', ') : majors[0];
        }
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
  methods: {

  },
};
</script>
