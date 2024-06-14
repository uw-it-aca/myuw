<template>
  <uw-card
    v-if="showCard"
    :loaded="showContent"
    :errored="isErrored"
    :errored-show="false"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Deciding on a Major</h2>
    </template>

    <template #card-body>
      <p class="myuw-text-md">
        Depending on what major you&rsquo;re interested in,
        <strong>you may need to begin planning now.</strong>
        Here are some ways to get started!
      </p>
    </template>

    <template #card-disclosure>
      <uw-collapse id="collapseDeclareMajor" v-model="isOpen">
        <div class="row gx-md-4">
          <div class="col-12 order-xl-2 col-xl-4 mb-xl-0 mb-3 mt-4">
            <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1">
              Current Major
            </h3>
            <div class="myuw-text-md">
              <cur_majors :term-majors="termMajors"></cur_majors>
            </div>
            <div v-if="hasRegHolds">
              <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1 mt-4">
                <span v-if="bothell">105 Credit Rule Status</span>
                <span v-else>Satisfactory Progress Status</span>
              </h3>
              <span class="badge bg-danger-light fw-normal myuw-text-md text-danger text-wrap p-2"
              >Registration Hold - <a :href="reviewOptionsUrl" class="link-danger"
              ><strong>Review options</strong></a></span>
            </div>
          </div>
          <div class="col-12 order-xl-1 col-xl-8">
            <h3 class="h6 myuw-font-encode-sans">Why plan ahead?</h3>
            <ul class="list-style myuw-text-md">
              <li>
                <strong v-if="bothell">105-Credit Rule:</strong>
                <strong v-else>Satisfactory Progress Policy (SPP):</strong> By the
                time students have earned 105 credits <em>AND</em> completed 5 quarters
                at the university, students are expected
                to declare a major or they receive a registration hold.
              </li>
              <li>
                <strong>Transfer Students:</strong> Transfer students who enter with <em>105 or more
                credits</em> are expected to declare a major before registering for their second
                quarter at the UW.
              </li>
            </ul>
          </div>
        </div>
        <hr />
        <major-bot v-if="bothell" />
        <major-tac v-else-if="tacoma" />
        <major-sea v-else />
        <div>
          <h3 class="h6 myuw-font-encode-sans">Interested in a particular major?</h3>
          <ul v-if="bothell" class="list-style myuw-text-md">
            <li><a href="https://uwb.navigate.eab.com/">Meet with your advisor</a> – Get in depth
              answers to your questions and make a plan to apply or declare.</li>
            <li><a href="https://www.uwb.edu/advising/majors-and-minors">How and when to declare
              a major</a> – Learn all about applying for and declaring a major.</li>
            <li><a href="https://myplan.uw.edu/program/#/orgs">Check your progress toward a degree
               in MyPlan</a> – Compare degree requirements to classes you’ve taken.</li>
            <li>Consider multiple majors and embrace a wider perspective – Capacity-constrained
              majors can be selective, take a holistic approach and reflect on what a meaningful
              path looks like to you.</li>
          </ul>
          <ul v-else class="list-style myuw-text-md">
            <li v-if="seattle">
              <a
                href="http://www.washington.edu/uaa/advising/degree-overview/majors/list-of-undergraduate-majors/"
              >Explore the major</a>
              – Learn how to declare or apply.
            </li>
            <li v-if="tacoma">
              <a
                href="https://www.tacoma.uw.edu/home/schools-and-programs"
              >Explore the major</a>
              – The process to declare or apply varies across each major.
            </li>
            <li>
              <a v-if="seattle"
                href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
              >Meet with a major adviser</a>
              <a v-if="tacoma"
                href="https://www.tacoma.uw.edu/gaa"
              >Meet with a major advisor</a>
              – Get in depth answers to your questions.
            </li>
            <li v-if="seattle">
              <a href="https://dawgpath.uw.edu/">Explore DawgPath</a>
              – Discover majors, average GPA at declaration, and explore career outcomes.
            </li>
            <li v-if="seattle">
              <a href="https://myplan.uw.edu/program/#/orgs">Find programs and check progress</a>
              - Filter by admission type and compare degree requirements to classes you’ve taken.
            </li>
            <li v-if="tacoma">
              <a href="https://myplan.uw.edu/program/#/orgs">Find programs and check progress</a>
              - Check your progress toward the degree.
            </li>
            <li>
              Consider multiple majors – Capacity-constrained majors can be selective, consider
              other majors that may align with your future goals.
            </li>
          </ul>
        </div>
        <div>
          <h3 class="h6 myuw-font-encode-sans">Get Help and Support</h3>
          <p class="list-style myuw-text-md">
            Navigating majors can be overwhelming, you’re not alone! If you have questions,
            <a v-if="seattle" href="https://my.uw.edu/academics/">reach out to your adviser</a>
            <a v-if="tacoma" href="https://www.tacoma.uw.edu/advising">reach out to your advisor</a>
            <a v-if="bothell" href="https://uwb.navigate.eab.com/">reach out to your advisor</a>
            who can give you personalized guidance based on your unique situation.
          </p>
        </div>
      </uw-collapse>
    </template>

    <template #card-footer>
      <button
        v-uw-collapse.collapseDeclareMajor
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Learn more about how to get started
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
// MUWM-5144 Pre-application
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';
import Collapse from '../../_templates/collapse.vue';
import CurMajors from '../../_common/cur_major.vue';
import MajorInfoSea from './major-sea.vue';
import MajorInfoBot from './major-bot.vue';
import MajorInfoTac from './major-tac.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
    'cur_majors': CurMajors,
    'major-sea': MajorInfoSea,
    'major-bot': MajorInfoBot,
    'major-tac': MajorInfoTac,
  },
  data() {
    return {
      isOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    ...mapState({
      classLevel: (state) => state.user.affiliations.class_level,
      seattle: (state) => state.user.affiliations.seattle,  // MUWM-5288
      bothell: (state) => state.user.affiliations.bothell, // MUWM-5296
      tacoma: (state) => state.user.affiliations.tacoma,  // MUWM-5297
    }),
    ...mapState('notices', {
      notices: (state) => state.value,
    }),
    ...mapState('profile', {
      profile: (state) => state.value,
      termMajors: (state) => state.value.term_majors,
    }),
    ...mapGetters('notices', {
      isNoticeFetching: 'isFetching',
      isNoticeReady: 'isReady',
      isNoticeErrored: 'isErrored',
    }),
    ...mapGetters('profile', {
      isProfileFetching: 'isFetching',
      isProfileReady: 'isReady',
      isProfileErrored: 'isErrored',
    }),
    regHoldsNotices() {
      return this.notices.filter((notice) =>
        notice.location_tags.includes('reg_card_holds'),
      );
    },
    hasRegHolds() {
      return this.regHoldsNotices.length > 0;
    },
    isJunior() {
      return this.classLevel === 'JUNIOR';
    },
    isSenior() {
      return this.classLevel === 'SENIOR';
    },
    isSophomore() {
      return this.classLevel === 'SOPHOMORE';
    },
    notDeclaredMajor() {
      // MUWM-5261
      return this.noDeclaredMajor(this.termMajors);
    },
    isTargetViewer() {
      return (
        (this.seattle || this.bothell) && (this.isJunior || this.isSenior) ||
         this.tacoma && (this.isSophomore || this.isJunior || this.isSenior));
    },
    showContent() {
      return (this.isNoticeReady && this.isProfileReady);
    },
    showCard() {
      return (this.notDeclaredMajor && this.isTargetViewer &&
        (this.isNoticeFetching || this.isProfileFetching || this.showContent));
    },
    isErrored() {
      return (this.isNoticesErrored || this.isProfileErrored);
    },
    reviewOptionsUrl () {
      return (this.tacoma ?
        "https://www.tacoma.uw.edu/registrar/academic-policies#permalink-16061"
        : this.bothell ?
          "https://www.uwb.edu/premajor/academic-advising/petitions"
          : "https://advising.uw.edu/academic-support/satisfactory-progress/"
      );
    },
  },
  created() {
    this.fetchProfile();
    this.fetchNotices();
  },
  methods: {
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('profile', {
      fetchProfile: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
