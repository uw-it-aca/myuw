<template>
  <uw-card v-if="showCard" :loaded="isReady">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation: Checklist</h2>
    </template>
    <template #card-body>
      <div class="row">
        <div class="col-8">
          <p>
            <strong>You're on your way!</strong> We're here to help you get to the finish line!
          </p>
          <p class = myuw-text-lg>
            Start with these Checklists
          </p>
          <ul class="list-style">
            <li>Review the
              <a href="https://www.washington.edu/students/graduation-checklist/">
              UW Graduation checklist
              </a> for an overview of tasks.
            </li>
            <li>International students, review the
              <a href="https://iss.washington.edu/resources/final-checklist/">
              ISS graduation checklist
              </a> for additional guidance.
            </li>
          </ul>
          <p class = myuw-text-lg>
            Take part in the commencement ceremonies
          </p>
          <p class = myuw-text-lg>
            Verify that your information and data will not be lost
          </p>
        </div>
        <div class="col-4">
          <p>
            <strong>Graduation application status</strong>
          </p>
          <p>
            <strong>Intended degree(s)</strong>
          </p>
        </div>
      </div>
    </template>
    <template #card-disclosure>
      <b-collapse
        id="collapseGradSupportAndHelp"
        v-model="isOpen"
      >
        <p>this is the disclosure content</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis dolorem labore a sit
          placeat nisi iusto ullam, ipsam vitae numquam ad, magni at ex quas ut magnam dignissimos
          incidunt nostrum.
        </p>
      </b-collapse>
    </template>
    <template #card-footer>
      <button
        v-b-toggle.collapseGradSupportAndHelp
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Learn how to get support and help
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
// MUWM-5009
import { mapGetters, mapState, mapActions } from 'vuex';
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data() {
    return {
      isOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      intlStudent: (state) => state.user.affiliations.intl_stud,
      classLevel: (state) => state.user.affiliations.class_level,
    }),
    ...mapState('profile', {
      degreeStatus: (state) => state.value.degree_status,
    }),
    showCard() {
      return (this.isReady && !this.degreeStatus.error_code);
    },
  },
  created() {
    if (this.classLevel === 'SENIOR') this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
</style>
