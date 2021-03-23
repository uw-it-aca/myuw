<template>
  <div>
    <h3 :class="{'sr-only': showRowHeader}">
      Enrollment
    </h3>
    <div v-if="useLegacyViewClasslist">
      <span>
        View class list in
        <b-link
          v-out="'Legacy myuw class list'"
          class="myuw-muted"
          :href="legacyLink"
          :title="`View ${section.id} class list`"
          target="_blank"
        >
          My Class Resources
        </b-link>
        <b-button :id="`cl_info_${section.id}`" variant="link">
          <font-awesome-icon :icon="faInfoCircle" />
          <span class="sr-only">More information</span>
        </b-button>
        <b-popover
          :target="`cl_info_${section.id}`"
          triggers="hover focus"
        >
          Class lists for independent study and secondary sections
          in previous quarters are only available via My Class Resources.
        </b-popover>
       </span>
    </div>

    <div v-else-if="section.isPrevTermEnrollment">
      <p>Registration opens
        {{  toFriendlyDate(section.registrationStart) }}
         at 6:00 AM PST.
      </p>
      <p>
        ({{section.current_enrollment}} of {{section.limit_estimate_enrollment}}
        students registered for course in
        {{ titleCaseWord(section.quarter) }} {{ section.year - 1 }})
      </p>
    </div>

    <div v-else-if="section.enrollment_student_name">
      <span>{{ section.enrollment_student_name }}</span>
      <b-link
        target="_blank"
        :href="`/teaching/${section.apiTag}/students`"
      >
        View student
      </b-link>
    </div>

    <div v-else>
      <span>
        {{ section.current_enrollment }}
        <span v-if="!section.is_independent_study">
          &nbsp;of&nbsp; {{ section.limit_estimate_enrollment }}
        </span>
      </span>

      <span>
        <b-link v-if="section.current_enrollment"
          target="_blank"
          :href="`/teaching/${section.apiTag}/students`"
        >
          View class list
        </b-link>
      </span>

      <span>
        <b-link v-if="displayDownloadLink"
          id="csv_download_class_list"
          :title="`Download ${section.id} class list`"
          @click="downloadCL"
        >
          <font-awesome-icon :icon="faDownload" /> Download (CSV)
        </b-link>
      </span>
    </div>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import {
  faDownload,
  faInfoCircle,
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
      faInfoCircle,
    };
  },
  computed: {
    ...mapState('classlist', {
      allData: (state) => state.value,
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
    }),
    getKey() {
      return this.section.apiTag.replace(/&amp;/g, '%26');
    },
    isDownloadPossible() {
      return this.isReadyTagged(this.getKey);
    },
    displayDownloadLink() {
      return (this.section.current_enrollment &&
        !this.section.isPrevTermEnrollment  &&
        this.isDownloadPossible);
    },
    sectionDetail() {
      return this.allData[this.getKey];
    },
    useLegacyViewClasslist() {
      return this.section.pastTerm && (
        this.section.is_independent_study ||
        !this.section.is_primary_section);
    },
    legacyLink() {
      return 'https://sdb.admin.uw.edu/sisMyUWClass/' +
      'uwnetid/pop/classlist.aspx?quarter=' +
      this.section.quarter + '+' +  this.section.year +
      '&sln=' + this.section.sln;
    }
  },
  created() {
    this.fetchClasslist(this.getKey);
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
    downloadCL() {
      this.downloadClassList(this.sectionDetail.sections[0]);
    },
  }
};
</script>
