<template>
  <div>
    <div class="w-100 myuw-border-top border-c7" />
    <img :src="uw_medicine_image" width="100px" alt="">
    <uw-card v-if="showCard"
             :loaded="isReady"
             :errored="isErrored"
             :errored-show="showError"
    >
      <template #card-heading>
        <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          UW Medicine Account
        </h3>
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
        <div v-if="med_pw_expired">
          <p>Password expired on {{ toFriendlyDate(expires_med) }}.
	          <a href="https://services.uwmedicine.org/passwordportal/login.htm" data-linklabel="Change UW Medicine Password" class="password-alert"><br>Change your password to regain access.</a>
          </p>
        </div>
        <div>
          <h4>
            Password expiration
          </h4>
          <div>
            
          </div>
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
  computed: {
    ...mapState({
      has_active_med_pw: (state) => state.profile.value.password.has_active_med_pw,
      med_pw_expired: (state) => state.profile.value.password.med_pw_expired,
      expires_med: (state) => state.profile.value.password.expires_med,
      uw_medicine_image: (state) => 'url(\'' + state.staticUrl + 'images/wday_logo.png\'',
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
      return true; //this.has_active_med_pw;
    },
  },
  mounted() {
    this.fetch()
  },
  methods: {
    toFriendlyDate(dateStr) {
      if (dateStr === undefined || dateStr.length === 0) {
        return '';
      }
      return dayjs(dateStr).format('ddd, MMM D');
    },
    ...mapActions('profile', ['fetch']),
  },
};
</script>
