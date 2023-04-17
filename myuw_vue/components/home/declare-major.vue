<template>
  <uw-card v-if="showCard" :loaded="showContent" :errored="isErrored" :errored-show="false">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Deciding on a Major</h2>
    </template>

    <template #card-body>
      <p class="myuw-text-md">
        Depending on what major you’re interested in,
        <strong>you may need to begin planning now.</strong> Here are some ways to get started!
      </p>
    </template>

    <template #card-disclosure>
      <uw-collapse id="collapseDeclareMajor" v-model="isOpen">
        <div class="row gx-md-4">
          <div class="col-12 order-xl-2 col-xl-4 mb-xl-0 mb-3">
            <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1">Current Major</h3>
            <div>
              <p class="myuw-text-md">print major and pending major here</p>
            </div>
            <h3 class="h6 text-dark myuw-font-encode-sans myuw-text-md mb-1">
              Satisfactory Progress Status
            </h3>
            <div>
              <p class="myuw-text-md">put hold info here</p>
            </div>
          </div>
          <div class="col-12 order-xl-1 col-xl-8">
            <h3 class="h6 myuw-font-encode-sans">Why plan ahead?</h3>
            <ul class="list-style myuw-text-md">
              <li>
                <strong>Satisfactory Progress Policy (SPP):</strong> By the time students have
                earned 105 credits AND completed 5 quarters at the university, students are expected
                to declare a major or they receive a registration hold
              </li>
              <li>
                <strong>Transfer Students:</strong> Transfer students who enter with 105 or more
                credits are expected to declare a major before registering for their second quarter
                at the UW
              </li>
            </ul>
          </div>
        </div>
        <hr />
        <div>
          <h3 class="h6 myuw-font-encode-sans">Unsure of what major to choose?</h3>
          <ul class="list-style myuw-text-md">
            <li>
              Talk to your pre-major adviser – Narrow down majors of interest, plan for alternate
              majors, and explore co-curricular opportunities
            </li>
            <li>bee boop</li>
          </ul>
        </div>
        <div>
          <h3 class="h6 myuw-font-encode-sans">Interested in a particular major?</h3>
          <ul class="list-style myuw-text-md">
            <li>
              Talk to your pre-major adviser – Narrow down majors of interest, plan for alternate
              majors, and explore co-curricular opportunities
            </li>
            <li>bee boop</li>
          </ul>
        </div>
        <div>
          <h3 class="h6 myuw-font-encode-sans">Get Help and Support</h3>
          <p class="list-style myuw-text-md">bee boop get help boop</p>
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
// import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import Collapse from '../_templates/collapse.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
  },
  data() {
    return {
      isOpen: false,
      showCard: true,
      showContent: true,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {},
  created() {},
  methods: {},
};
</script>

<style lang="scss" scoped></style>
