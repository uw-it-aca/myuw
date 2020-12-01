<template>
  <uw-card v-if="showCard"
           :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        UW NetID
      </h3>
    </template>
    <template #card-body>
      <div>
        <a href="https://uwnetid.washington.edu/manage/" target="_blank" title="Manage UW NetID"
           class="btn btn-outline-beige text-dark myuw-text-md mb-4"
        >
          Manage UW NetID account
        </a>
      </div>
      <div class="">
        <ul class="list-unstyled m-0 myuw-text-md">
          <li class="mb-1">
            <a href="https://uwnetid.washington.edu/manage/?password" target="_blank" title="Change UW NetID password">Change UW NetID password</a>
          </li>
          <li>
            <a href="https://identity.uw.edu/account/recovery/" target="_blank" title="NetID account recovery options">Set account recovery options</a>
          </li>
          <li v-if="two_factor" class="mt-1">
            <a href="https://identity.uw.edu/2fa/" target="_blank" title="Manage two-factor authentication">Manage two-factor authentication (2FA)</a>
          </li>
        </ul>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. Please
      try again later. In the meantime, if you want to change your password,
      try the <a href="https://uwnetid.washington.edu/manage/?password" data-linklabel="UW NetID page" target="_blank">UW NetID page</a>.
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
    ...mapGetters('profile', [
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showCard: function() {
      return !this.isReady ||
        !this.isHomePage ||
        !this.applicant && !this.employee && !this.student;
    },
    showError: function() {
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
