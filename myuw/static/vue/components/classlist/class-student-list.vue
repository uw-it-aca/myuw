<template>
  <uw-card v-if="instructor && showContent"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="isErrored"
  >
    <template #card-heading>
      <div v-if="sectionData">
        <h3>
          {{ sectionData.currAbbr }} {{ sectionData.courseNum }}
          {{ sectionData.sectionId }},
          {{ sectionData.quarter }} {{ sectionData.year }}
        </h3>
        <div>
          <h4>SLN</h4>
          <span>{{ sectionData.sln }}</span>
        </div>
      </div>
    </template>

    <template #card-body>
      <uw-course-stats
        v-if="sectionData.current"
        :curr-abbr="sectionData.currAbbr"
        :course-num="sectionData.courseNum"
        :section-id="sectionData.sectionId"
        :quarter="sectionData.quarter"
        :year="sectionData.year"
        :current-student-majors="sectionData.sections[0].current_student_majors"
      />
      <div id="classlist_controls">
        <div role="tablist" aria-label="Views">
          <div>
            <a id="list_view"
               href="#" role="tab"
               aria-controls="classlist_table_view"
               aria-selected="true"
            >
              <i class="fa fa-table" aria-hidden="true" />Table
            </a>
          </div>

          <div>
            <a id="grid_view"
               href="#" role="tab"
               aria-controls="classlist_photogrid_view"
               aria-selected="false"
            >
              <i class="fa fa-user-circle-o" aria-hidden="true" />Photo Grid
            </a>
          </div>
        </div>

        <div>
          <div id="class-list-sort-controls">
            <label for="sort_list">Sort: </label>
            <select id="sort_list" class="">
              <option value="surname,first_name" selected="selected">
                Last Name
              </option>
              <option value="first_name,surname">
                First Name
              </option>
              <option value="netid">
                UW NetID
              </option>
              <option value="class_code">
                Class
              </option>
              <option value="credits">
                Credits
              </option>

              <option v-if="sectionData.sections[0].has_linked_sections"
                      value="linked_sections"
              >
                Secondary Section
              </option>
            </select>
          </div>

          <button v-if="sectionData.sections[0].has_joint"
                  id="toggle_joint"
                  type="button" class=""
                  aria-pressed="false"
                  title="Show students from joint courses"
          >
            <i class="fa fa-square-o" aria-hidden="true" />
            Joint Course Students
          </button>
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

      <uw-table-content :section="sectionData.sections[0]" />
    </template>

    <template v-if="noData" #card-error>
      No class information was found.
    </template>
    <template v-else-if="noAccessPermission" #card-error>
      You need to be the class instructor to view student information.
    </template>
    <template v-else-if="invalidCourse" #card-error>
      The page you seek is for a past quarter and is no longer available.
    </template>
    <template v-else-if="dataError" #card-error>
      An error occurred and MyUW cannot load the class student information
      right now. Please try again later.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import CourseStats from './statistics.vue';
import Content from './content.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-stats': CourseStats,
    'uw-table-content': Content,
  },
  props: {
    sectionLabel: {
      type: String,
      required: true,
    },
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      instructor: (state) => state.user.affiliations.instructor,
    }),
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    getKey() {
      return this.sectionLabel.replace(/&amp;/g, '%26');
    },
    isReady() {
      return this.isReadyTagged(this.getKey);
    },
    sectionData() {
      return this.allData[this.getKey];
    },
    isErrored() {
      return this.isErroredTagged(this.getKey);
    },
    showContent() {
      return !this.isReady || this.isErrored ||
        this.sectionData && this.sectionData.sections.length &&
        this.sectionData.sections[0].registrations.length;
    },
    getErrorCode() {
      return this.statusCodeTagged(this.getKey);
    },
    noAccessPermission() {
      return this.getErrorCode === 403;
    },
    noData() {
      return this.getErrorCode === 404;
    },
    invalidCourse() {
      return this.getErrorCode === 410;
    },
    dataError() {
      return this.isErrored && !(this.noData ||
        this.noAccessPermission || this.invalidCourse);
    },
  },
  created() {
    if (this.instructor) {
      this.fetchClasslist(this.getKey);
    }
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
  },
};
</script>
