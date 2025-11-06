<template>
  <div v-if="showCard">
    <div class="w-100 myuw-border-top border-c7" />
    <uw-card :loaded="isReady"
             :errored="isErrored"
             :errored-show="showError"
    >
      <template #card-heading>
        <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          UW Medicine Account
        </h2>
        <img :src="staticUrl+'images/UWMedicine_Logo_RGB@2x.png'"
             width="100px"
             alt=""
             class="position-absolute"
        >
      </template>
      <template #card-error>
        An error occurred and MyUW cannot load your information right now.
        <!--
        In the meantime, try the <a href="passwordChange">UW Medicine Account</a> page.
        -->
      </template>
      <template #card-body>
        <p>
          This password is for UW Medicine applications
          like Epic, ORCA, MINDscape, AMC network, etc.
        </p>
        <div v-if="expired">
          <div class="alert alert-danger" role="alert">
            <p>
              Password expired on {{ toFriendlyDate(expiresMed) }}.
              <!--
              <br>
              <a v-out="'Change UW Medicine password'" :href="passwordChange">
                Change your password to regain access.
              </a>
              -->
            </p>
          </div>
        </div>
        <div v-else>
          <uw-card-status>
            <template #status-label>
              Password expiration
            </template>
            <template #status-value>
              <uw-formatted-date
                :due-date="expiresMed"
                :display-text-danger="true"
                :display-time="true">
              </uw-formatted-date>
            </template>
            <template #status-content>
              <div class="text-end">
                {{ toFromNowDate(expiresMed) }}*
              </div>
            </template>
          </uw-card-status>
          <p class="text-muted myuw-text-md">
            *Expiration date gets updated nightly.
          </p>
          <!--
          <a :href="passwordChange">Change UW Medicine password</a>
          -->
        </div>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import CardStatus from '../_templates/card-status.vue';
import Card from '../_templates/card.vue';
import FormattedDate from '../_common/formatted-date.vue';


export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-formatted-date': FormattedDate,
  },
  computed: {
    ...mapState({
      password: (state) => state.profile.value.password,
      staticUrl: (state) => state.staticUrl,
    }),
    ...mapGetters('profile', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    showError() {
      return this.statusCode !== 404;
    },
    hasActiveMedPw() {
      return Boolean(this.password.last_change_med);
    },
    expiresMed() {
      return this.password.expires_med;
    },
    showCard() {
      return (!this.isReady ||
        Boolean(this.password) && this.hasActiveMedPw && Boolean(this.expiresMed));
    },
    expired() {
      return this.timeDeltaFrom(this.expiresMed, 'second') < 0;
    },
    passwordChange() {
      return 'https://sailpoint.uwmedicine.org/';
    }
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('profile', {
      fetch: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
img {
  top: 1rem;
  right: 1rem;
}
</style>
