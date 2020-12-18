<template>
  <div>
    <div>
      <b-button
        v-if="section.has_joint"
        id="toggle_joint"
        :pressed.sync="showJointCourse"
        title="Show students from joint courses"
        variant="light"
      >
        <i class="fa fa-square-o" aria-hidden="true" />
        Joint Course Students
      </b-button>
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

    <div class="">
      <a id="download_class_list" href="#" class="">
        <i class="fa fa-download" />Download (CSV)
      </a>

      <a href="javascript:window.print()" class="">
        <i class="fa fa-print" />Print
      </a>
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
    switchView: function(event) {
      alert('Switch ');
    },
  },
};
</script>
