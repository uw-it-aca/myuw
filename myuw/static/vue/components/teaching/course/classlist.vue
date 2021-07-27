<template>
  <uw-card-property-group>
    <uw-card-property title="Enrollment">
      <template v-if="useLegacyViewClasslist">
        <span>
          View class list in
          <b-link
            v-out="'Legacy myuw class list'"
            class="myuw-muted"
            :href="legacyLink"
            :title="`View class list of ${section.label}`"
          >
            My Class Resources
          </b-link>
          <button :id="`cl_info_${section.id}`" type="button"
           class="btn btn-link"
          >
            <font-awesome-icon :icon="faInfoCircle" />
            <span class="sr-only">More information</span>
          </button>
          <b-popover
            :target="`cl_info_${section.id}`"
            triggers="hover focus"
          >
            Class lists for independent study and secondary sections
            in previous quarters are only available via My Class Resources.
          </b-popover>
        </span>
      </template>

      <template v-else-if="section.isPrevTermEnrollment">
        <p>Registration opens
          {{  toFriendlyDate(section.registrationStart) }}
          at 6:00 AM PST.
        </p>
        <p>
          ({{section.current_enrollment}} of {{section.limit_estimate_enrollment}}
          students registered for course in
          {{ titleCaseWord(section.quarter) }} {{ section.year - 1 }})
        </p>
      </template>

      <template v-else-if="section.enrollment_student_name">
        <span>{{ section.enrollment_student_name }}</span>
        <b-link
          :href="`/teaching/${section.apiTag}/students`"
          :title="`View class list of ${section.label}`"
        >
          View student
        </b-link>
      </template>

      <template v-else>
        <span class="mr-3">
          {{ section.current_enrollment }}
          <span v-if="!section.is_independent_study">
            &nbsp;of&nbsp; {{ section.limit_estimate_enrollment }}
          </span>
        </span>

        <span class="mr-3">
          <b-link v-if="section.current_enrollment"
            :href="`/teaching/${section.apiTag}/students`"
            :title="`View class list of ${section.label}`"
          >
            View class list
          </b-link>
        </span>

        <span class="mr-3">
          <b-link v-if="displayDownloadLink"
            id="csv_download_class_list"
            :title="`Download class list of ${section.label}`"
            @click="downloadCL"
          >
            <font-awesome-icon :icon="faDownload" /> Download (CSV)
          </b-link>
        </span>
      </template>
    </uw-card-property>
  </uw-card-property-group>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import {
  faDownload,
  faInfoCircle,
} from '@fortawesome/free-solid-svg-icons';
import CardPropertyGroup from '../../_templates/card-property-group.vue';
import CardProperty from '../../_templates/card-property.vue';

export default {
  components: {
    'uw-card-property-group': CardPropertyGroup,
    'uw-card-property': CardProperty,
  },
  props: {
    section: {
      type: Object,
      required: true,
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
