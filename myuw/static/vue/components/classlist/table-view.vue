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
      <b-table striped hover :fields="fields" :items="items">
        <template #cell(email)="data">
          <a href="`mailto:${data.item.email}`"
             title="`Email ${data.item.firstName} ${data.item.surName}`"
          >
            <i class="fa fa-envelope-o" />
            <span class="sr-only">{{ data.item.email }}</span>
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
  },
  computed: {
    fields() {
      let data = [
        {
          key: 'studentNumber',
          label: 'Student No.',
          sortable: true,
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
      if (this.section.has_joint) {
        data.push(
            {
              class: 'joint',
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
          sortable: true,
        }],
      );
      if (this.section.is_independent_start) {
        data = data.concat([
          {
            key: 'startDate',
            label: 'Start Date',
            sortable: true,
          },
          {
            key: 'endDate',
            label: 'End Date',
            sortable: true,
          }],
        );
      }
      data.push(
          {
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
        if (this.section.has_joint) {
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
        let majors = '';
        for (let j = 0; j < reg.majors.length; j++) {
          if (j < reg.majors.length -1) {
            majors = majors.concat(',&nbsp;');
          }
          majors = majors.concat(this.ucfirst(reg.majors[j].name));
        }
        dataItem.majors = majors;
        if (this.section.is_independent_start) {
          dataItem.startDate = reg.start_date;
          dataItem.endDate = reg.end_date;
        }
        dataItem.email = reg.email;
        console.log(dataItem);
        data.push(dataItem);
      }
      return data;
    },
  },
  methods: {
    getClass(reg) {
      return reg.is_joint ? 'joint' : '';
    },
  },
};
</script>
