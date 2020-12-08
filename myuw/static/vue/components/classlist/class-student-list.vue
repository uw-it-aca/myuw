<template>
  <uw-card v-if="showContent"
           :loaded="isReadyTagged"
           :errored="isErroredTagged"
           :errored-show="showError"
  >
    <template v-if="showContent" #card-heading>
      <h3>
        {{ sectionData.currAbbr }} {{ sectionData.courseNum }}
        {{ sectionData.sectionId }},
        {{ sectionData.quarter }} {{ sectionData.year }}
      </h3>
      <div>
        <h4>SLN</h4>
        <span>{{ sectionData.sln }}</span>
      </div>
    </template>
    <template v-else-if="isErroredTagged" #card-heading>
      <h3>Class List of {{ sectionLabel.replace(/[,/]/g, ' ') }}</h3>
    </template>

    <template #card-body>
      YES!
    </template>

    <template v-if="noData" #card-error>
      No class information was found.
    </template>
    <template v-else-if="noAccesssPermission" #card-error>
      You need to be the class instructor to view student information.
    </template>
    <template v-else-if="invalidCourse" #card-error>
      The page you seek is for a past quarter and is no longer available.
    </template>
    <template v-else-if="showError" #card-error>
      An error occurred and MyUW cannot load the class student information
      right now. Please try again later.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
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
      sectionData(state) {
        return state.value[this.sectionLabel];
      },
    }),
    ...mapGetters('classlist', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
      statusCodeTagged: 'statusCodeTagged',
    }),
    getUrlSuffix() {
      return this.sectionLabel.replace(/&amp;/g, '%26');
    },
    isReady() {
      return this.isReadyTagged(this.getUrlSuffix());
    },
    showContent() {
      return this.instructor && this.sectionData.sections.length;
    },
    isErrored() {
      return this.isErroredTagged(this.getUrlSuffix());
    },
    getErrorCode() {
      return this.statusCodeTagged(this.getUrlSuffix());
    },
    noAccessPermission() {
      return this.getErrorCode() === 403;
    },
    noData() {
      return this.getErrorCode() === 404;
    },
    invalidCourse() {
      return this.getErrorCode() === 410;
    },
    showError() {
      return !this.nodData() && !this.noAccessPermission() &&
        !this.invalidCourse();
    },
  },
  created() {
    if (this.instructor) {
      this.fetchClasslist(this.getUrlSuffix());
    }
  },
  methods: {
    ...mapActions('classlist', {
      fetchClasslist: 'fetch',
    }),
  },
};
</script>
