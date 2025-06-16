<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">U-Pass Membership</h2>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your U-PASS status right now. In the meantime,
      you may find what you need on the
      <a href="https://transportation.uw.edu/getting-here/transit/u-pass">U-PASS</a> page.
    </template>
    <template #card-body>
      <uw-card-status>
        <template #status-label>Status</template>
        <template #status-value>
          {{ isActive ? 'Current' : 'Not current' }}
        </template>
      </uw-card-status>

      <div v-if="isActive" id="upass-notices">
        <a :href="getTroubleshootingUrl" class="myuw-text-md">
          U-PASS not working?
        </a>
        <br>
        <a v-out="'What is U-PASS'" :href="getWhatIsUrl" class="myuw-text-md">
          What is the U-PASS?
        </a>
      </div>
      <div v-else id="upass-not-current">
        <div v-if="!student && employee">
          <p class="myuw-text-md">
            Some employees automatically qualify for a
            <a v-out="'Subsidized U-PASS'" href="https://hr.uw.edu/policies/u-pass/eligibility/">
              subsidized U-PASS</a>.
            If you do not qualify, you can purchase a quarterly or annual U-PASS
            through your <a v-out="'campus transportation office'"
                            :href="getEmployeePurchaseUrl">campus transportation office</a>.
          </p>
        </div>
        <div v-if="student" id="upass-notices-for-students">
          <div v-if="(seattle || tacoma) && !pce" class="myuw-text-md">
            <p>
              If you are registered for a quarter, your U-PASS will work one week
              before the quarter starts.
            </p>
          </div>
          <div v-else id="upass-notices-for-non-sea-studs">
            <p v-if="bothell || pce" class="myuw-text-md">
              If you
              <a v-out="'Purchase U-PASS'" :href="getPurchaseUrl">
                purchase</a>
              a U-PASS for a quarter, your U-PASS will work one week before the quarter starts.
            </p>
          </div>
        </div>
        <div v-if="student && inSummer && !bothell">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans">
            Summer U-PASS Use
          </h3>
          <p class="myuw-text-md">
            Unless you are registered for summer quarter, your U-PASS will not
            work during summer quarter. Check your
            <a
              v-out="'campus transportation office'"
              :href="getSummerPurchaseUrl"
            >
              campus transportation office</a> for summer transit options.
          </p>
        </div>
        <ul class="list-unstyled myuw-text-md mb-1">
          <li class="mb-1">
            <a v-out="'What is U-PASS'" :href="getWhatIsUrl" class="myuw-text-md">
              What is the U-PASS?
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
    ...mapGetters('upass', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      employee: (state) => state.user.affiliations.all_employee,
      student: (state) => state.user.affiliations.student,
      tacoma: (state) => state.user.affiliations.tacoma,
      bothell: (state) => state.user.affiliations.bothell,
      seattle: (state) => state.user.affiliations.seattle,
      pce: (state) => state.user.affiliations.pce,
      status: (state) => state.upass.value,
    }),
    isActive() {
      return this.status.active_employee_membership || this.status.active_student_membership;
    },
    inSummer() {
      return this.status.in_summer;
    },
    showCard() {
      return this.employee || this.student;
    },
    showError() {
      return this.statusCode !== 404;
    },
    getTroubleshootingUrl() {
      return this.bothell
        ? 'mailto:uwbpark@uw.edu?subject=ORCA Question'
        : this.tacoma
          ? 'https://www.tacoma.uw.edu/fa/facilities/transportation/frequently-asked-questions#permalink-16642'
          : 'https://transportation.uw.edu/getting-here/transit/u-pass#troubleshooting';
    },
    getPurchaseUrl() {
      return this.bothell
        ? 'https://www.uwb.edu/commuter-services/transportation/upass'
        : 'https://www.pce.uw.edu/help/registration-costs/costs-and-fees';
    },
    getWhatIsUrl() {
      return this.tacoma
        ? 'https://www.tacoma.uw.edu/fa/facilities/transportation/u-pass-benefits'
        : this.bothell
          ? 'https://www.uwb.edu/commuter-services/transportation/upass'
          : 'https://transportation.uw.edu/getting-here/transit/u-pass';
    },
    getSummerPurchaseUrl() {
      return this.tacoma
        ? 'https://www.tacoma.uw.edu/fa/facilities/transportation/universal-u-pass'
        : this.bothell
          ? 'https://www.uwb.edu/commuter-services/transportation/upass'
          : 'https://transportation.uw.edu/getting-here/transit/u-pass#u-pass-students';
    },
    getEmployeePurchaseUrl(){
      return this.tacoma
        ? 'https://www.tacoma.uw.edu/fa/facilities/transportation/employee-u-pass-order-form'
        : this.bothell
          ? 'https://www.uwb.edu/commuter-services/transportation/upass'
          : 'https://transportation.uw.edu/getting-here/transit/u-pass';
    }
  },
  created() {
    if (this.employee || this.student) this.fetch();
  },
  methods: {
    ...mapActions('upass', ['fetch']),
  },
};
</script>
