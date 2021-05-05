<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">UW NetID</h2>
    </template>
    <template #card-body>
      <p>
        <uw-link-button href="https://uwnetid.washington.edu/manage/">
          Manage UW NetID account
        </uw-link-button>
      </p>
      <div class="">
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a
              href="https://uwnetid.washington.edu/manage/?password"
              title="Change UW NetID password"
            >Change UW NetID password</a>
          </li>
          <li>
            <a
              href="https://identity.uw.edu/account/recovery/"
              title="NetID account recovery options"
            >Set account recovery options</a>
          </li>
          <li v-if="two_factor" class="mt-1">
            <a
              href="https://identity.uw.edu/2fa/"
              title="Manage two-factor authentication"
            >Manage two-factor authentication (2FA)</a>
          </li>
        </ul>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. Please try again later. In
      the meantime, if you want to change your password, try the
      <a href="https://uwnetid.washington.edu/manage/?password">UW NetID</a> page.
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link-button': LinkButton,
  },
  props: {
    isHomePage: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState({
      data: (state) => {
        return state.profile.value.password;
      },
      two_factor: (state) => state.user.affiliations['2fa_permitted'],
      applicant: (state) => state.user.affiliations.applicant,
      employee: (state) => state.user.affiliations.employee,
      student: (state) => state.user.affiliations.student,
    }),
    ...mapGetters('profile', ['isReady', 'isErrored', 'statusCode']),
    showCard: function () {
      return !this.isHomePage || (!this.applicant && !this.employee && !this.student);
    },
    showError: function () {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', ['fetch']),
  },
};
</script>
