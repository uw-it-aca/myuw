<template>
  <uw-card v-if="showCard"
   :loaded="isReady"
   :errored="isErrored"
   :errored-show="showError"
  >
    <template #card-heading>
      <h3>
        Housing &amp; Food Services
      </h3>
    </template>
    <template #card-error>
      <p>
        <i class="fa fa-exclamation-triangle" />
        An error occurred and MyUW cannot load your information right now.
        In the meantime, try the
        <a href="https://hfs.uw.edu/myhfs/account.aspx"
           data-linklabel="Housing & Food Services"
           target="_blank"
        >
          Housing &amp; Food Services
        </a>.
      </p>
    </template>
    <template #card-body>
      <div v-if="hfs.resident_dining">
        <div>
          <h4>Dining Balance</h4>
        </div>
        <div>
          <span>${{ hfs.resident_dining.balance.toFixed(2) }}</span>
        </div>
      </div>

      <div>
        <h4>Explore Campus Housing</h4>
        <ul>
          <li>
            <a href="https://www.hfs.uw.edu"
               data-linklabel="Housing & Food Services"
            >
              Housing &amp; Food Services
            </a>
          </li>
          <li>
            <a href="https://www.trumba.com/calendars/sea_hfs"
               data-linklabel="HFS Dates and Deadlines"
            >
              Dates and Deadlines
            </a>
          </li>
          <li>
            <a href="https://ucharm.hfs.washington.edu/ucharm"
               data-linklabel="Apply for Campus Housing"
            >
              Apply for Campus Housing
            </a>
          </li>
          <li>
            <a href="mailto:hfsinfo@uw.edu"
               data-linklabel="Contact HFS"
            >
              Contact Us
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h4>Manage Account</h4>
        <ul class="unstyled-list">
          <li>
            <a href="https://www.hfs.uw.edu/myhfs/account.aspx"
               data-linklabel="HFS: Make a Payment"
            >
              Make a Payment
            </a>
          </li>
          <li>
            <a href="https://www.hfs.uw.edu/myhfs/ledger.aspx"
               data-linklabel="HFS: View Charges"
            >
              View Charges
            </a>
          </li>
          <li>
            <a href="https://www.hfs.uw.edu/myhfs/dininglevel"
               data-linklabel="HFS: Change Dining Level"
            >
              Change Dining Level
            </a>
          </li>
          <li>
            <a href="https://ucharm.hfs.washington.edu/ucharm"
               data-linklabel="Update HFS Account"
            >
              Update Account
            </a>
          </li>
        </ul>
      </div>
      <div>
        <h4>Resident Resources</h4>
        <ul>
          <li>
            <a href="https://mc360.maytag.com/#/"
               data-linklabel="Check Laundry Status"
            >
              Check Laundry Status
            </a>
          </li>
          <li>
            <a href="https://fms.admin.uw.edu/fs-works/uwnetid"
               data-linklabel="HFS: Submit a Work Order"
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
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
export default {
  components: {
    'uw-card': Card,
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
      showCard: (state) => (state.user.affiliations.seattle && (
        state.user.affiliations.undergrad || state.user.affiliations.grad )
      ),
      showError: function() {
        return this.statusCode !== 404;
      },
    }),
    showError: function() {
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


