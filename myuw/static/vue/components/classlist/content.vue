<template>
  <div>
    <div>
      <b-form-checkbox
        v-if="section.has_joint"
        id="toggle_joint"
        v-model="showJointCourse"
        :title="buttonTitle(showJointCourse)"
      >
        Joint Course Students
      </b-form-checkbox>
    </div>

    <div class="">
      <b-link
        id="csv_download_class_list"
        @click="downloadClassList"
      >
        <i class="fa fa-download" />Download (CSV)
      </b-link>

      <a href="javascript:window.print()" class="">
        <i class="fa fa-print" />Print
      </a>
    </div>

    <div id="classlist_controls">
      <b-tabs role="tablist" aria-label="Views">
        <b-tab title="Table" active>
          <uw-table-view
            :section="section"
            :show-joint-course-stud="showJointCourse"
          />
        </b-tab>
        <b-tab title="Photo Grid">
          <uw-photo-list
            :registrations="section.registrations"
            :show-joint-course-stud="showJointCourse"
          />
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
import TableView from './table-view.vue';
import PhotoList from './photo-list.vue';

export default {
  components: {
    'uw-table-view': TableView,
    'uw-photo-list': PhotoList,
  },
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
  data() {
    return {
      showJointCourse: false,
    };
  },
  methods: {
    buttonTitle(showJointCourse) {
      return (showJointCourse ?
        'To hide students from joint courses' :
        'To show students from joint courses');
    },
    fileName() {
      const fn = this.section.section_label + '_students.csv';
      return fn.replace(/[^a-z0-9._]/ig, '_');
    },
    downloadClassList() {
      const hiddenElement = document.createElement('a');
      const csvData = this.buildClasslistCsv(
          this.section.registrations, this.section.has_linked_sections);

      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvData);
      hiddenElement.target = '_blank';
      hiddenElement.download = this.fileName;
      hiddenElement.click();
    },
  },
};
</script>
