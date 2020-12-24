<template>
  <div v-if="showCard">
    <div class="w-100 myuw-border-top border-c7" />
    <uw-card :loaded="isReady"
             :errored="isErrored"
             :errored-show="showError"
    >
      <template #card-heading>
        <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          UW Medicine Account
        </h3>
        <img :src="staticUrl+'images/UWMedicine_Logo_RGB@2x.png'"
             width="100px"
             alt=""
        >
      </template>
      <template #card-error>
        An error occurred and MyUW cannot load your information right now.
        In the meantime, try the
        <a href="https://services.uwmedicine.org/passwordportal/login.htm"
           data-linklabel="UW Medicine account site"
           target="_blank"
        >UW Medicine Account page</a>.
      </template>
      <template #card-body>
        <p>
          This password is for UW Medicine applications
          like Epic, ORCA, MINDscape, AMC network, etc.
        </p>
        <div v-if="medPwExpired">
          <!--TODO: Maybe use a b-alert..?-->
          <b-alert show variant="danger">
            <p>
              Password expired on {{ toFriendlyDate(expiresMed) }}.
              <a :href="passwordChange"
                 data-linklabel="Change UW Medicine Password"
              >
                <br>Change your password to regain access.
              </a>
            </p>
          </b-alert>
        </div>
        <div v-else>
          <h4>
            Password expiration
          </h4>
          <div :class="expires30Days ? 'text-danger' : ''">
            <span>{{ toFriendlyDate(expiresMed) }}</span>
            <span>in {{ daysBeforeExpires }} days*</span>
          </div>
          <p>*Expiration date gets updated nightly.</p>
          <a :href="passwordChange"
             target="_blank"
          >
            Change UW Medicine password
          </a>
        </div>
      </template>
    </uw-card>
  </div>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import dayjs from 'dayjs';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {
      passwordChange: 'https://services.uwmedicine.org/passwordportal/login.htm',
    };
  },
  computed: {
    ...mapState({
      hasActiveMedPw: (state) => state.profile.value.password.has_active_med_pw,
      medPwExpired: (state) => state.profile.value.password.med_pw_expired,
      expiresMed: (state) => state.profile.value.password.expires_med,
      daysBeforeExpires: (state) => {
        return state.profile.value.password.days_before_med_pw_expires;
      },
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
    showCard() {
      return !this.isReady || (this.isReady && this.hasActiveMedPw);
    },
    expires30Days() {
      return this.daysBeforeExpires <= 30;
    },
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
