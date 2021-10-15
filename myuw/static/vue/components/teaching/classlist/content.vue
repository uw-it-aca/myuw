<template>
  <div>
    <div class="myuw-print-hidden mt-2" :class="$mq === 'mobile' ? '' : 'float-right'">
      <div class="myuw-text-md align-middle">
        <b-form-checkbox
          v-if="section.has_joint && isJointSectionDataReady"
          id="toggle_joint"
          v-model="showJointCourse"
          inline
          :title="buttonTitle(showJointCourse)"
        >
          Joint Course Students
        </b-form-checkbox>

        <a class="mr-2" @click="downloadCL">
          <font-awesome-icon :icon="faDownload" />
          Download (CSV)
        </a>

        <a
          href="javascript:window.print()" class="">
          <font-awesome-icon :icon="faPrint" /> Print
        </a>
      </div>
    </div>

    <b-tabs
      title="Views"
      pills
      nav-wrapper-class="mb-3 p-0 myuw-print-hidden"
      active-nav-item-class="bg-transparent rounded-0
      myuw-border-bottom border-dark text-body font-weight-bold"
    >
      <b-tab
        title-item-class="text-nowrap myuw-text-md mr-2 mb-1"
        title-link-class="rounded-0 px-2 py-1 h-100 text-body myuw-border-bottom"
        active
      >
        <template #title>
          <font-awesome-icon :icon="faTable" /> Table
        </template>
        <uw-table-view
          :section="section"
          :show-joint-course-stud="showJointCourse"
        />
      </b-tab>
      <b-tab
        title-item-class="text-nowrap myuw-text-md mr-2 mb-1"
        title-link-class="rounded-0 px-2 py-1 h-100 text-body myuw-border-bottom"
      >
        <template #title>
          <font-awesome-icon :icon="faUserCircle" /> Photo Grid
        </template>
        <uw-photo-list
          :registrations="section.registrations"
          :show-joint-course-stud="showJointCourse"
        />
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import {
  faDownload,
  faPrint,
  faTable,
  faUserCircle,
} from '@fortawesome/free-solid-svg-icons';
import TableView from './table-view.vue';
import PhotoList from './photo-list.vue';

export default {
  components: {
    'uw-table-view': TableView,
    'uw-photo-list': PhotoList,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showJointCourse: false,
      faDownload,
      faPrint,
      faTable,
      faUserCircle,
    };
  },
  computed: {
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
    }),
    isJointSectionDataReady() {
      let ret = true;
      this.section.joint_sections.forEach((section) => {
        ret = ret && (
          this.isReadyTagged[section.url] ||
          this.isErroredTagged[section.url]);
      });
      return ret;
    },
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
