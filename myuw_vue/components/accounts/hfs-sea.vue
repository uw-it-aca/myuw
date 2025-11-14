<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Housing &amp; Food Services
      </h2>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. In the meantime, try the
      <a
        href="https://hfs.uw.edu/myhfs/account.aspx"
      > Housing &amp; Food Services</a> page.
    </template>
    <template #card-body>
      <uw-card-status v-if="hfs.resident_dining">
        <template #status-label>Dining Balance</template>
        <template #status-value> ${{ hfs.resident_dining.balance.toFixed(2) }} </template>
      </uw-card-status>

      <div>
        <ul class="list-unstyled myuw-text-md">
          <li class="mb-1">
            <a href="https://hfs.uw.edu">Explore campus housing &amp; dining</a>
          </li>
          <li class="mb-1">
            <a href="https://hfs.uw.edu/uw-housing-guides"
            >View UW housing guides</a>
          </li>
          <li class="mb-1">
            <a href="https://www.trumba.com/calendars/sea_hfs"
            >Dates, deadlines and events</a>
          </li>
          <li class="mb-1">
            <a href="https://washington.starrezhousing.com/StarRezPortalX/"
            >Apply for housing and manage your account</a>
          </li>
          <li class="mb-1">
            <a href="mailto:hfsinfo@uw.edu">Contact HFS</a>
          </li>
          <li class="mb-1">
            <a href="https://washington.assetworks.cloud/ready/"
            >Submit a work order</a>
          </li>
        </ul>
      </div>
    </template>
  </uw-card>
</template>
<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
  },
  computed: {
    ...mapState('hfs', {
      hfs: (state) => state.value,
    }),
    ...mapGetters('hfs', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      seattle: (state) => state.user.affiliations.seattle,
      undergrad: (state) => state.user.affiliations.undergrad,
      grad: (state) => state.user.affiliations.grad,
    }),
    showCard() {
      return this.seattle && (this.undergrad || this.grad);
    },
    showError() {
      return this.statusCode !== 404;
    },
  },
  mounted() {
    this.fetchHfs();
  },
  methods: {
    ...mapActions('hfs', {
      fetchHfs: 'fetch',
    }),
  },
};
</script>


