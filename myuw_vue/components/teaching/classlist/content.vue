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

        <button class="me-2" @click="downloadCL">
          <font-awesome-icon :icon="faDownload" />
          Download (CSV)
        </button>

        <button @click="printPhotos">
          <font-awesome-icon :icon="faPrint" /> Print
        </button>
      </div>
    </div>

    <uw-tabs
      pills
      bottom-border
      nav-wrapper-class="mb-3 p-0 myuw-print-hidden"
    >
      <template #tabs>
        <uw-tab-button panel-id="table"
            title-item-class="me-2 mb-1"
            title-link-class="rounded-0 text-body">
          <font-awesome-icon
            :icon="faTable"
            class="align-baseline"
          />
          Table
        </uw-tab-button>
        <uw-tab-button panel-id="photo-grid"
            title-item-class="me-2 mb-1"
            title-link-class="rounded-0 text-body">
          <font-awesome-icon
            :icon="faUserCircle"
            class="align-baseline"
          />
          Photo Grid
        </uw-tab-button>
      </template>
      <template #panels>
        <uw-tab-panel panel-id="table">
          <uw-table-view :section="section" :show-joint-course-stud="showJointCourse" />
        </uw-tab-panel>
        <uw-tab-panel panel-id="photo-grid">
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
import { mapState, mapMutations } from 'vuex';
import { faDownload, faPrint, faTable, faUserCircle } from '@fortawesome/free-solid-svg-icons';
import Tabs from '../../_templates/tabs/tabs.vue';
import TabButton from '../../_templates/tabs/button.vue';
import TabPanel from '../../_templates/tabs/panel.vue';
import TableView from './table-view.vue';
import PhotoList from './photo-list.vue';

export default {
  components: {
    'uw-tabs': Tabs,
    'uw-tab-button': TabButton,
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
  computed: {
    ...mapState({
      activePanel: (state) => state.activePanel,
    }),
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
    printPhotos() {
      this.addVarToState({
        name: 'activePanel',
        value: this.activePanel,
      });
      window.print();
    },
    ...mapMutations([
      'addVarToState',
    ]),
  },
};
</script>
