<template>
  <uw-card
    v-if="showCard"
    :loaded="showContent"
    :errored="isErroredAdvisers || isErroredProfile"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Advisers
      </h2>
    </template>
    <template #card-body>
      <div v-if="hasAdviser">
        <ul class="d-flex flex-wrap list-unstyled mb-0">
          <li
            v-for="(adviser, index) in advisers"
            :key="index"
            class="mb-3"
            :class="[$mq === 'mobile' ? 'w-100' : 'w-50']"
          >
            <div class="myuw-text-md">
              <div
                class="fw-bold myuw-font-encode-sans"
              >{{ adviser.program }}</div>
              <div>{{ adviser.full_name }}
                <span v-if="adviser.pronouns">({{ adviser.pronouns }})</span>
              </div>
              <div>{{ adviser.email_address }}</div>
              <div>{{ formatPhoneNumberDisaply(adviser.phone_number) }}</div>
              <div v-if="adviser.booking_url">
                <a :href="adviser.booking_url">Make an appointment online</a>
              </div>
            </div>
          </li>
        </ul>
        <hr class="my-0 bg-secondary">
      </div>
      <div v-if="profile.campus === 'Seattle'" class="myuw-text-md mt-3 mb-3">
        <div class="fw-bold myuw-font-encode-sans"
        >Departmental and Major Advising Offices</div>
        <a
          href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
        >View departmental and major advising offices’ contact information</a>
      </div>

       <!--Tacoma without assigned advisor-->
       <div v-if="profile.campus === 'Tacoma'" class="myuw-text-md mt-3 mb-3">
        <a
          href="https://www.tacoma.uw.edu/gaa#permalink-37917"
        >Find an advising office's contact information</a>
      </div>

      <!--Bothell without assigned advisor-->
       <div v-if="profile.campus === 'Bothell'" class="myuw-text-md mt-3 mb-3">
        <a
          href="https://uwb.navigate.eab.com/"
        >Find your academic adviser's contact information</a>
      </div>

      <hr v-if="hasMajors || hasMinors" class="my-0 bg-secondary">
      <uw-card-property v-if="hasMajors" title="Your Major" class="mt-3" :no-margin-bottom="true">
          <ul class="list-unstyled">
            <template v-for="(termMajor, index) in termMajors">
              <li v-if="index == 0" :key="index" class="mb-1">
                {{ degreeListString(termMajor.majors) }}
              </li>
              <li v-else-if="termMajor.degrees_modified" :key="index" class="mb-1">
                Beginning {{ titleCaseWord(termMajor.quarter) }} {{ termMajor.year }}:
                &nbsp;&nbsp;
                <span v-if="termMajor.majors.length > 0">
                  {{ degreeListString(termMajor.majors) }}
                </span>
                <span v-else>
                  None
                </span>
              </li>
            </template>
          </ul>
      </uw-card-property>
      <uw-card-property v-if="hasMinors" title="Your Minor">
          <ul class="list-unstyled mb-0">
            <template v-for="(termMinor, index) in termMinors">
              <li v-if="index == 0 && termMinor.minors.length" :key="index" class="mb-1">
                {{ degreeListString(termMinor.minors) }}
              </li>
              <li v-else-if="termMinor.degrees_modified" :key="index" class="mb-1">
                Beginning {{ titleCaseWord(termMinor.quarter) }} {{ termMinor.year }}:
                &nbsp;&nbsp;
                <span v-if="termMinor.minors.length > 0">
                  {{ degreeListString(termMinor.minors) }}
                </span>
                <span v-else class="text-muted">
                  None
                </span>
              </li>
            </template>
          </ul>
      </uw-card-property>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your adviser information right now.
      In the meantime, to contact a general adviser, try the
      <a href="https://www.washington.edu/uaa/advising/">
        Undergraduate Advising
      </a> page and to contact a departmental or major adviser, try the
      <a href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/">
        Departmental and Major Advising Offices
      </a> page.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';
export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
  },
  computed: {
    ...mapState({
      isUndergrad: (state) => state.user.affiliations.undergrad,
      studEmployee: (state) => state.user.affiliations.stud_employee,
      isPCE: (state) => state.user.affiliations.pce,
      isApplicant: (state) => state.user.affiliations.applicant,
      isGrad: (state) => state.user.affiliations.grad,
      advisers: (state) => state.advisers.value,
      profile: (state) => state.profile.value,
    }),
    ...mapGetters('advisers', {
      isFetchingAdvisers: 'isFetching',
      isErroredAdvisers: 'isErrored',
      statusCodeAdvisers: 'statusCode',
    }),
    ...mapGetters('profile', {
      isFetchingProfile: 'isFetching',
      isErroredProfile: 'isErrored',
      statusCodeProfile: 'statusCode',
    }),
    shouldLoad() {
      return !this.isPCE && (this.isUndergrad || this.studEmployee) && !this.isGrad;
    },
    termMajors() {
      return this.profile.term_majors;
    },
    termMinors() {
      return this.profile.term_minors;
    },
    hasMinors() {
      return (this.termMinors && this.termMinors.length &&
        this.termMinors[0].minors && this.termMinors[0].minors.length > 0);
    },
    hasMajors() {
      return (this.termMajors && this.termMajors.length &&
        this.termMajors[0].majors && this.termMajors[0].majors.length > 0);
    },
    showError() {
      return (
        this.isErroredAdvisers && this.statusCodeAdvisers != 404 ||
        this.isErroredProfile && this.statusCodeProfile != 404
      );
    },
    hasAdviser() {
      return this.advisers && this.advisers.length > 0;
    },
    hasProfile() {
      return (
        this.profile &&
        this.profile.campus !== undefined &&
        (this.profile.class_level === 'FRESHMAN' ||
         this.profile.class_level === "SOPHOMORE" ||
         this.profile.class_level === "JUNIOR" ||
         this.profile.class_level === "SENIOR")
      );  //MUWM-5349
    },
    showContent() {
      return this.hasAdviser || this.hasProfile;
    },
    showCard() {
      return (
        this.shouldLoad &&
        (this.isFetchingAdvisers || this.isFetchingProfile || this.showContent ||
         this.showError));
    }
  },
  created() {
    if (this.shouldLoad) {
      this.fetchAdvisers();
      this.fetchProfile();
    }
  },
  methods: {
    ...mapActions('advisers', {
      fetchAdvisers: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
  },
};
</script>
