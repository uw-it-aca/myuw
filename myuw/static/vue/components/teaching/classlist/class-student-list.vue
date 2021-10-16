<template>
  <div>
    <uw-card v-if="showCard"
            :loaded="isReady"
            :errored="isErrored"
            no-bottom-margin
            class="myuw-printable-card"
            style="max-width: 100vw; overflow-x: hidden;"
    >
      <template #card-heading>
        <div v-if="sectionData" class="d-flex flex-wrap justify-content-between">
          <h2
            class="h3 text-dark-beige myuw-font-encode-sans"
            :class="[$mq === 'mobile' ? 'w-100' : '']"
          >
            {{ sectionData.currAbbr }} {{ sectionData.courseNum }}
            {{ sectionData.sectionId }},
            {{ titleCaseWord(sectionData.quarter) }} {{ sectionData.year }}
          </h2>
          <span v-if="sectionData.sln">
            SLN {{ sectionData.sln }}
          </span>
        </div>
      </template>

      <template #card-body>
        <uw-classlist-content
          :section="sectionData.sections[0]"
          :isJointSectionDataReady="isJointSectionDataReady" />
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

    <uw-course-stats
      :loaded="isReady"
      :section-data="sectionData ? sectionData : {}"
    />
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../_templates/card.vue';
import CourseStats from './statistics.vue';
import Content from './content.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-course-stats': CourseStats,
    'uw-classlist-content': Content,
  },
  props: {
    sectionLabel: {
      type: String,
      required: true,
    },
  },
  data: function() {
    return {
      isLoadedJointRegLinkedSection: false,
      isJointSectionDataReady: false,
    };
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
      isFetchingTagged: 'isFetchingTagged',
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
      return this.sectionData && this.sectionData.sections.length &&
        this.sectionData.sections[0].registrations.length;
    },
    showCard() {
      return this.instructor &&
        (!this.isReady || this.isErrored || this.showContent);
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
    jointSections() {
      return this.sectionData.sections[0].joint_sections;
    },
  },
  watch: {  // MUWM-4385
    isReady: function (newValue, oldValue) {
      if (this.showContent && this.jointSections) {
        if (!this.isLoadedJointRegLinkedSection) {
          this.loadJointRegLinkedSection();
          this.isLoadedJointRegLinkedSection = true;
        }
      }
    },
    isLoadedJointRegLinkedSection: function (newValue, oldValue) {
      this.isJointSectionDataReady = this.isJointDataReady();
    }
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
    loadJointRegLinkedSection() {  // MUWM-4385
      this.jointSections.forEach((section) => {
        this.fetchClasslist(section.url);
      });
    },
    isJointDataReady() {  // MUWM-4385
      let ret = true;
      for (let i = 0; i < this.jointSections.length; i++) {
        const section = this.sectionData.sections[0].joint_sections[i];
        const fetch = this.isFetchingTagged[section.url];
        const ready = this.isReadyTagged[section.url];
        const error = this.isErroredTagged[section.url];
        ret = ret && (ready || error);
      }
      return Boolean(ret);
    },
  },
};
</script>
