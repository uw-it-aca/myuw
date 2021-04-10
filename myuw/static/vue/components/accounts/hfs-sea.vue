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
      >
        Housing &amp; Food Services </a
      >.
    </template>
    <template #card-body>
      <uw-card-status v-if="hfs.resident_dining">
        <template #status-label>Dining Balance</template>
        <template #status-value> ${{ hfs.resident_dining.balance.toFixed(2) }} </template>
      </uw-card-status>

      <div>
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          Explore Campus Housing
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li>
            <a href="https://www.hfs.uw.edu">
              Housing &amp; Food Services
            </a>
          </li>
          <li>
            <a v-out="'HFS: Dates and Deadlines'"
              href="https://www.trumba.com/calendars/sea_hfs"
            >
              Dates and Deadlines
            </a>
          </li>
          <li>
            <a v-out="'HFS: Apply for Campus Housing'"
              href="https://ucharm.hfs.washington.edu/ucharm"
            >
              Apply for Campus Housing
            </a>
          </li>
          <li>
            <a href="mailto:hfsinfo@uw.edu">Contact HFS </a>
          </li>
        </ul>
      </div>
      <div>
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          Manage Account
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li>
            <a v-out="'HFS: Make a Payment'"
              href="https://www.hfs.uw.edu/myhfs/account.aspx"
            >
              Make a Payment
            </a>
          </li>
          <li>
            <a v-out="'HFS: View Charges'"
              href="https://www.hfs.uw.edu/myhfs/ledger.aspx">
              View Charges
            </a>
          </li>
          <li>
            <a v-out="'HFS: Change Dining Level'"
              href="https://www.hfs.uw.edu/myhfs/dininglevel"
            >
              Change Dining Level
            </a>
          </li>
          <li>
            <a v-out="'HFS: Update Account'"
              href="https://ucharm.hfs.washington.edu/ucharm">
              Update Account
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h3 class="h6 text-dark-beige myuw-font-encode-sans">
          Resident Resources
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <li>
            <a v-out="'HFS: Check Laundry Status'"
              href="https://mc360.maytag.com/#/">
              Check Laundry Status
            </a>
          </li>
          <li>
            <a v-out="'HFS: Submit a Work Order'"
              href="https://fms.admin.uw.edu/fs-works/uwnetid"
            >
              Submit a Work Order
            </a>
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
    showCard: function () {
      return this.seattle && (this.undergrad || this.grad);
    },
    showError: function () {
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


