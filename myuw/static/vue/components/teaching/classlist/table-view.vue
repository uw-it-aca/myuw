<template>
  <div>
    <h3 class="sr-only">
      Table of Student Information
    </h3>
    <uw-table :fields="fields" :items="items">
      <template #default="slotProps">
        <div
          v-if="slotProps.cellData.key == 'linkedSection' ||
                slotProps.cellData.key == 'credits'"
          class="text-center"
        >
          {{slotProps.cellData.value}}
        </div>
        <div v-else-if="slotProps.cellData.key == 'email'"
          class="text-center"
        >
          <a
            v-inner="'Email student'"
            :href="slotProps.cellData.value.href"
            :title="slotProps.cellData.value.title"
          >
            <font-awesome-icon :icon="faEnvelope" class="myuw-print-hidden" />
            <span style="overflow-wrap: break-word;" class="sr-only myuw-print-sr-only">
              {{ slotProps.cellData.value.email }}
            </span>
          </a>
        </div>
        <template v-else>
          {{ slotProps.cellData.value }}
        </template>
      </template>
    </uw-table>
  </div>
</template>
<script>
import {mapState} from 'vuex';
import {
  faEnvelope,
} from '@fortawesome/free-solid-svg-icons';
import Table from '../../_templates/card-table.vue';
export default {
  components: {
    'uw-table': Table,
  },
  props: {
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
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
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
          key: 'firstName',
          label: 'First Name',
          sortable: true,
        },
        //{
        //  key: 'Pronouns',
        //  label: 'Pronouns',
        //  sortable: true,
        //},
      ];
      if (this.showJointCourseStud) {
        data.push(
            {
              key: 'jointCourse',
              label: 'Joint Course',
              sortable: true,
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
          //Pronouns: reg.pronouns,
        };
        if (this.showJointCourseStud) {
          dataItem.jointCourse = reg.isJoint ? reg.sectionLabel : this.section.label;
        }
        if (this.section.has_linked_sections) {
          if (reg.isJoint && this.showJointCourseStud) {
            // MUWM-4385
            dataItem.linkedSection = this.getRegisteredLinkedSection(reg.sectionLabel, reg.netid);
          } else {
            dataItem.linkedSection = reg.linked_sections;
          }
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
  methods: {
    // MUWM-4385
    getRegisteredLinkedSection(jointSectionLabel, netid) {
      let linkedSectionId = '';
      this.section.joint_sections.forEach((section) => {
        if (jointSectionLabel === section.label) {
          if (this.allData[section.url]) {
            this.allData[section.url].sections[0].registrations.forEach((reg) => {
              if (reg.netid === netid) {
                linkedSectionId = reg.linked_sections;
                return;
              }
            });
          }
          return;
        }
      });
      return linkedSectionId;
    },
  },
};
</script>
