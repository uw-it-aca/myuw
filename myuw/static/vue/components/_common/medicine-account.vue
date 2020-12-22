<template>
  <div>
    <div class="w-100 myuw-border-top border-c7" />
    <uw-card v-if="showCard"
             :loaded="isReady"
             :errored="isErrored"
             :errored-show="showError"
    >
      <template #card-heading>
        <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
          UW Medicine Account
        </h3>
        <img :src="staticUrl+'images/UWMedicine_Logo_RGB@2x.png'" width="100px" alt="">
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
          <!--Maybe add a b-alert instead..?-->
          <p>Password expired on {{ toFriendlyDate(expires_med) }}.
	          <a href="https://services.uwmedicine.org/passwordportal/login.htm" data-linklabel="Change UW Medicine Password" class="password-alert"><br>Change your password to regain access.</a>
          </p>
        </div>
        <div v-else>
          <h4>
            Password expiration
          </h4>
          <component :is="expires_30_days ? b-alert : div"
                     :variant="expires_30_days ? danger : ''"
                     show
          >
            <span>{{ toFriendlyDate(expires_med) }}</span>
            <span>in {{ days_before_expires }} days*</span>
          </component>
          <!--
          <b-alert v-if="expires_30_days" show variant="danger">
            
          </b-alert>
          <div v-else>
            <span>{{ toFriendlyDate(expires_med) }}</span>
            <span>in {{ days_before_expires }} days*</span>
          </div>
          <p>*Expiration date gets updated nightly.</p>
          <a href="https://services.uwmedicine.org/passwordportal/login.htm">Change UW Medicine password</a>
        -->
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
      time_stamp: (state) => state.profile.value.password.time_stamp,
      days_before_expires: (state) => {
        console.log(daysjs(time_stamp).diff(expires_med, 'day'));
        return daysjs(time_stamp).diff(expires_med, 'day');
      },
      expires_30_days: (state) => {
        return this.days_before_expires <= 30;
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
      return !this.isReady || (this.isReady && this.has_active_med_pw);
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
    ...mapActions('profile', {
      fetch: 'fetch',
    }),
  },
};
</script>
