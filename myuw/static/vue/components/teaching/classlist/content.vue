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
        v-out="'Download Classlist CSV'"
        @click="downloadCL"
      >
        <font-awesome-icon :icon="faDownload" />
        Download (CSV)
      </b-link>

      <a
        v-out="'Print Classlist'"
        href="javascript:window.print()" class="">
        <i class="fa fa-print" />Print
      </a>
    </div>

    <div id="classlist_controls">
      <b-tabs role="tablist" title="Views">
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
import {
  faDownload,
} from '@fortawesome/free-solid-svg-icons';
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
      faDownload,
    };
  },
  methods: {
    buttonTitle(showJointCourse) {
      return (showJointCourse ?
        'To hide students from joint courses' :
        'To show students from joint courses');
    },
    downloadCL() {
      this.downloadClassList(this.section);
    },
  },
};
</script>
