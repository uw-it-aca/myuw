<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
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
      <a href="https://transportation.uw.edu/"
        data-linklabel="UW Transportation Service"
        target="_blank"
      >UW Transportation page</a>.
    </template>
    <template #card-body>
      <h4>Status</h4>
      <span>{{ is_current ? 'Current' : 'Not current' }}</span>

      <div v-if="is_current" id="upass-notices">
        <p v-if="display_activation">
          Finalize activation by tapping your card on a reader.
        </p>
        <div v-if="!employee && in_summer && (pce || seattle)">
          <h4>Summer U-PASS Use</h4>
          <p>
            Your U-PASS does not work during summer quarter unless you are registered
            for a class or are a
            <a href="https://facilities.uw.edu/transportation/employee-u-pass#8"
              data-linklabel="TEMP Pass"
            >
              temporary employee
            </a>.
          </p>
        </div>
        <a :href="getUrl" data-linklabel="U-Pass">
          U-PASS not working?
        </a>
      </div>
      <div v-else id="upass-not-current">
        <div v-if="!employee" id="upass-notices-for-students">
          <div v-if="seattle">
            <p>
              If you are registered for a quarter, your U-PASS will work one week before
              the quarter starts.
            </p>
            <div v-if="in_summer">
              <h4>Summer U-PASS Use</h4>
              <p>
                Your U-PASS does not work during summer quarter unless you are registered
                for a class or are a
                <a
                  href="https://facilities.uw.edu/transportation/employee-u-pass#8"
                  data-linklabel="Temporary Employee U-PASS"
                >
                  temporary employee
                </a>.
              </p>
            </div>
          </div>
          <div v-else id="upass-notices-for-non-sea-studs">
            <p v-if="(bothell || tacoma)">
              If you <a :href="getPurchaseUrl" data-linklabel="Purchase U-PASS">purchase</a>
              a U-PASS for a quarter, your U-PASS will work one week before the quarter starts.
            </p>
          </div>
        </div>
        <ul>
          <li>
            <a :href="getWhatIsUrl" data-linklabel="What is U-PASS">
              What is the U-PASS?
            </a>
          </li>
          <li v-if="pce">
            <a href="https://facilities.uw.edu/transportation/student-purchased-u-pass"
                  data-linklabel="CC Student Purchase U-PASS"
            >
              Purchasing a U-PASS
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
    ...mapGetters('upass', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      student: (state) => state.user.affiliations.student,
      tacoma: (state) => state.user.affiliations.tacoma,
      bothell: (state) => state.user.affiliations.bothell,
      seattle: (state) => state.user.affiliations.seattle,
      pce: (state) => state.user.affiliations.pce,
      display_activation: (state) => state.upass.value.display_activation,
      in_summer: (state) => state.upass.value.in_summer,
      is_current: (state) => state.upass.value.is_current,
    }),
    showCard() {
      return this.employee || this.student;
    },
    showError() {
      return this.statusCode !== 404;
    },
    getUrl() {
      if (this.employee) {
        return "https://facilities.uw.edu/transportation/employee-u-pass#10";
      }
      return (
        this.bothell ? "https://www.uwb.edu/facility/commuter-services/upass" : (
          this.tacoma ? "https://www.tacoma.uw.edu/getting-campus/u-pass-orca" :
            "https://facilities.uw.edu/transportation/student-u-pass#3"));
    },
    getPurchaseUrl() {
      return (this.bothell ? "https://www.uwb.edu/facility/commuter-services/upass" :
        "https://www.tacoma.uw.edu/getting-campus/students-purchasing-u-pass");
    },
    getWhatIsUrl() {
      if (this.employee) {
        return "http://www.washington.edu/u-pass";
      }
      return (
        this.tacoma ?  "https://www.tacoma.uw.edu/getting-campus/what-u-pass" : (
          this.bothell ? "https://www.uwb.edu/facility/commuter-services/upass" : (
            this.seattle ? "https://facilities.uw.edu/transportation/student-u-pass" : (
              this.pce ?  "https://facilities.uw.edu/transportation/student-u-pass#9" :
                "http://www.washington.edu/u-pass/"))));
      }
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
