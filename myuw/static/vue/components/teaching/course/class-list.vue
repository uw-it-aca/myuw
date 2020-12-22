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
            <button v-if="isDownloadPossible" @click="downloadClassList">
              <font-awesome-icon :icon="faDownload" /> Download (CSV)
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import {
  faDownload,
} from '@fortawesome/free-solid-svg-icons';

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
      faDownload,
    };
  },
  computed: {
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
    }),
    sectionDetail() {
      return this.allData[this.sectionLabel];
    },
    sectionLabel() {
      let s = this.section;
      return `${s.year},${s.quarter.toLowerCase()},${s.curriculum_abbr},${
        s.course_number
      }/${s.section_id}`;
    },
    isDownloadPossible() {
      return this.isReadyTagged(this.sectionLabel);
    }
  },
  created() {
    this.fetchClasslist(this.sectionLabel);
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
    fileName() {
      const fn = this.section.section_label + '_students.csv';
      return fn.replace(/[^a-z0-9._]/ig, '_');
    },
    downloadClassList() {
      const hiddenElement = document.createElement('a');
      const csvData = this.buildClasslistCsv(
        this.sectionDetail.section[0].registrations,
        this.sectionDetail.section[0].has_linked_sections
      );

      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvData);
      hiddenElement.target = '_blank';
      hiddenElement.download = this.fileName();
      hiddenElement.click();
    },
  }
};
</script>
