<template>
  <div>
    <div class="myuw-print-hidden mt-2" :class="$mq === 'mobile' ? '' : 'float-end'">
      <div class="myuw-text-md align-middle">
        <div v-if="section.has_joint && isJointSectionDataReady"
          class="form-check form-check-inline">
          <input
            id="toggle_joint"
            v-model="showJointCourse"
            class="form-check-input"
            type="checkbox"
            :title="buttonTitle(showJointCourse)"
          />
          <label class="form-check-label" for="toggle_joint">
            Joint Course Students
          </label>
        </div>

        <a class="me-2" @click="downloadCL">
          <font-awesome-icon :icon="faDownload" />
          Download (CSV)
        </a>

        <a href="javascript:window.print()" class="">
          <font-awesome-icon :icon="faPrint" /> Print
        </a>
      </div>
    </div>

    <uw-tabs
      title="Views"
      pills
      bottom-border
      nav-wrapper-class="mb-3 p-0 myuw-print-hidden"
    >
      <template #tabs>
        <uw-tab-list-button content-id="tab1">
          <font-awesome-icon
            :icon="faTable"
            class="align-baseline text-mid-beige myuw-text-tiny"
          />
          Table
        </uw-tab-list-button>
        <uw-tab-list-button content-id="tab2">
          <font-awesome-icon
            :icon="faUserCircle"
            class="align-baseline text-mid-beige myuw-text-tiny"
          />
          Photo Grid
        </uw-tab-list-button>
      </template>
      <template #panels>
        <uw-tab-panel content-id="tab1">
          <uw-table-view :section="section" :show-joint-course-stud="showJointCourse" />
        </uw-tab-panel>
        <uw-tab-panel content-id="tab2">
          <uw-photo-list
            :registrations="section.registrations"
            :show-joint-course-stud="showJointCourse"
          />
        </uw-tab-panel>
      </template>
    </uw-tabs>
  </div>
</template>

<script>
import { faDownload, faPrint, faTable, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import Tabs from '../../_templates/tabs/tab-container.vue';
import TabListButton from '../../_templates/tabs/tab-list-button.vue';
import TabPanel from '../../_templates/tabs/tab-panel.vue';
import TableView from './table-view.vue';
import PhotoList from './photo-list.vue';

export default {
  components: {
    'uw-tabs': Tabs,
    'uw-tab-list-button': TabListButton,
    'uw-tab-panel': TabPanel,
    'uw-table-view': TableView,
    'uw-photo-list': PhotoList,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    isJointSectionDataReady: {
      type: Boolean,
      required: true,
    }
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
  methods: {
    buttonTitle(showJointCourse) {
      return showJointCourse
        ? 'To hide students from joint courses'
        : 'To show students from joint courses';
    },
    downloadCL() {
      this.downloadClassList(this.section);
    },
  },
};
</script>
