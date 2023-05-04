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
            <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1 mt-4">
              Satisfactory Progress Status
            </h3>
            <span v-if="hasRegHolds"
              class="badge bg-danger-light fw-normal myuw-text-md text-danger text-wrap p-2">
              Registration Hold -
              <strong>
                <a
                  href="https://www.washington.edu/uaa/advising/academic-support/satisfactory-progress/"
                  class="link-danger"
                >Review options</a>
              </strong>
            </span>
          </div>
          <div class="col-12 order-xl-1 col-xl-8">
            <h3 class="h6 myuw-font-encode-sans">Why plan ahead?</h3>
            <ul class="list-style myuw-text-md">
              <li>
                <strong>Satisfactory Progress Policy (SPP):</strong> By the
                time students have earned 105 credits <em>AND</em> completed 5 quarters
                at the university, students are expected
                to declare a major or they receive a registration hold.
              </li>
              <li>
                <strong>Transfer Students:</strong> Transfer students who enter with <em>105 or more
                credits</em> are expected to declare a major before registering for their second quarter
                at the UW.
              </li>
            </ul>
          </div>
        </div>
        <hr />
        <div class="mt-4">
          <h3 class="h6 myuw-font-encode-sans">Unsure of what major to choose?</h3>
          <ul class="list-style myuw-text-md">
            <li>
              <a href="https://www.washington.edu/uaa/advising/appointments/"
                >Talk to your pre-major adviser</a
              >
              – Narrow down majors of interest, plan for alternate majors, and explore co-curricular
              opportunities.
            </li>
            <li>
              <a href="https://www.washington.edu/uaa/advising/guides/overview/"
                >Review UW Advising's Guides</a
              >
              – Explore activities and questions like, “What majors are you finding yourself curious
              about?” and “Can you articulate why you plan to choose a particular major?”
            </li>
            <li>
              <a href="https://uw.pathwayu.com/">Gain insight with PathwayU</a> – Discover your
              purpose, interests, values, and workplace preferences.
            </li>
            <li>
              <a
                href="https://my.uw.edu/husky_experience_message?article=mapping-interests-and-values-meaningful-work"
                >Consider a wider perspective</a
              >
              – Take a holistic approach and reflect on what a meaningful path looks like to you.
            </li>
            <li>
              <a href="https://www.washington.edu/uaa/advising/degree-overview/majors/"
                >Learn more about the major</a
              >
              – Pre-majors, double majors, and admission types.
            </li>
          </ul>
        </div>
        <div>
          <h3 class="h6 myuw-font-encode-sans">Interested in a particular major?</h3>
          <ul class="list-style myuw-text-md">
            <li>
              <a
                href="http://www.washington.edu/uaa/advising/degree-overview/majors/list-of-undergraduate-majors/"
                >Explore the major</a
              >
              – Learn how to declare or apply.
            </li>
            <li>
              <a
                href="http://www.washington.edu/uaa/advising/degree-overview/majors/advising-offices-by-program/"
                >Meet with a major adviser</a
              >
              – Get in depth answers to your questions.
            </li>
            <li>
              <a href="https://dawgpath.uw.edu/">Explore DawgPath</a> – Discover majors, average GPA
              at declaration, and explore career outcomes.
            </li>
            <li>
              <a href="https://myplan.uw.edu/program/#/orgs">Find programs and check progress</a> –
              Filter by admission type and compare degree requirements to classes you’ve taken.
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
            <a href="https://my.uw.edu/academics/">reach out to your adviser</a> who can give you
            personalized guidance based on your unique situation.
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

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
    'cur_majors': CurMajors,
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
      return (this.classLevel === 'JUNIOR');
    },
    showCard() {
      return (this.isJunior &&
        (this.isNoticeFetching || this.isProfileFetching ||
         this.showContent));
    },
    showContent() {
      return (this.isNoticeReady && this.isProfileReady);
    },
    isErrored() {
      return (this.isNoticesErrored || this.isProfileErrored);
    },
  },
  created() {
    this.fetchNotices();
    this.fetchProfile();
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
