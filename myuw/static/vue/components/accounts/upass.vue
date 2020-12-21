<template>
  <uw-card :loaded="isReady"
           :errored="isErrored"
           :errored-show="showError"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        U-Pass Membership
      </h3>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your Husky card balance
      right now. In the meantime, if you want to add funds, try the
      <a href="http://facilities.uw.edu/transportation/index"
         data-linklabel="UW Transportation"
         target="_blank"
      >UW Transportation page</a>.
    </template>
    <template #card-body>
      <h4>
        Status
      </h4>
      <span>{{ is_current ? 'Current' : 'Not current' }}</span>

      <div v-if="is_current">
        <p v-if="display_activation">
          Finalize activation by tapping your card on a reader.
        </p>
        <div v-if="!is_employee && in_summer && (pce || seattle)">
          <h4>Summer U-PASS Use</h4>
          <p>Your U-PASS does not work during summer quarter unless you are registered for a class or are a <a href="https://facilities.uw.edu/transportation/employee-u-pass#8" data-linklabel="TEMP Pass">temporary employee</a>.</p>
        </div>
        <ul>
          <li>
            <a v-if="is_employee" href="https://facilities.uw.edu/transportation/employee-u-pass#10" data-linklabel="Employee U-Pass">U-PASS not working?</a>
            <a v-else-if="bothell" href="https://www.uwb.edu/facility/commuter-services/upass" data-linklabel="Bothell U-Pass">U-PASS not working?</a>
            <a v-else-if="tacoma" href="https://www.tacoma.uw.edu/getting-campus/u-pass-orca" data-linklabel="Tacoma U-Pass and ORCA">U-PASS not working?</a>
            <a v-else href="https://facilities.uw.edu/transportation/student-u-pass#3" data-linklabel="Student U-Pass">U-PASS not working?</a>
          </li>
        </ul>
      </div>
      <div v-else>
        <ul v-if="is_employee">
          <li><a href="http://www.washington.edu/u-pass">What is the U-PASS?</a></li>
        </ul>
        <div v-else-if="seattle">
          <p>
            If you are registered for a quarter, your U-PASS
            will work one week before the quarter starts.
          </p>
          <div v-if="in_summer">
            <h4>Summer U-PASS Use</h4>
            <p>Your U-PASS does not work during summer quarter unless you are registered for a class or are a <a href="https://facilities.uw.edu/transportation/employee-u-pass#8" data-linklabel="Temporary Employee U-Pass">temporary employee</a>.</p>
          </div>
        </div>
        <div v-else-if="bothell">
          <p>If you <a href="https://www.uwb.edu/facility/commuter-services/upass" data-linklabel="Purchase a U-Pass">purchase</a> a U-PASS for a quarter, your U-PASS will work one week before the quarter starts.</p>
        </div>
        <div v-else-if="tacoma">
          <p>If you <a href="https://www.tacoma.uw.edu/getting-campus/students-purchasing-u-pass" data-linklabel="Purchase a U-Pass">purchase</a> a U-PASS for a quarter, your U-PASS will work one week before the quarter starts.</p>
        </div>

        <ul v-if="pce">
          <li><a href="https://facilities.uw.edu/transportation/student-u-pass#9">What is the U-PASS?</a></li>
          <li><a href="https://facilities.uw.edu/transportation/student-purchased-u-pass">Purchasing a U-PASS</a></li>
        </ul>

        <ul v-else-if="seattle">
          <li><a href="https://facilities.uw.edu/transportation/student-u-pass">What is the U-PASS?</a></li>
        </ul>

        <ul v-else-if="tacoma">
          <li><a href="https://www.tacoma.uw.edu/getting-campus/what-u-pass">What is the U-PASS?</a></li>
        </ul>

        <ul v-else-if="!bothell">
          <li><a href="http://www.washington.edu/u-pass/">What is the U-PASS?</a></li>
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
    ...mapGetters('upass', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      tacoma: (state) => state.user.affiliations.tacoma,
      bothell: (state) => state.user.affiliations.bothell,
      seattle: (state) => state.user.affiliations.seattle,
      pce: (state) => state.user.affiliations.pce,
      display_activation: (state) => state.upass.value.display_activation,
      in_summer: (state) => state.upass.value.in_summer,
      is_current: (state) => state.upass.value.is_current,
      is_employee: (state) => state.upass.value.is_employee,
    }),
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('upass', {
      fetch: 'fetch',
    }),
  },
};
</script>
