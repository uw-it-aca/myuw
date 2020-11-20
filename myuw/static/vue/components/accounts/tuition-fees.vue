<template>
  <uw-card 
    v-if="isStudent"
    :loaded="isReadyNotices && isReadyTuition"
    :errored="isErroredNotices || isErroredTuition" 
    :erroredShow="showError"
  >
    <template #card-heading>
      <h3>
        Tuition &amp; Fees
      </h3>
    </template>
    <template #card-body>
      <div v-if="tuition.due_today">
        <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Tuition and fees are due today.
      </div>
      <div v-if="tuition.past_due">
        <i class="fa fa-exclamation-triangle" aria-hidden="true"></i> You have a balance that may be past due. See your statement for details.
      </div>

      <ul>
        <!-- If there is some or no tuition due -->
        <li v-if="tuition.tuition_accbalance >= 0">
          <div>
            <h4>Amount Due <br><span>Student Fiscal Services</span></h4>
					  <div v-if="tuition.tuition_accbalance > 0">
              <span>${{tuition.tuition_accbalance.toFixed(2)}}</span>
              <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx" target="_blank" data-linklabel="Tuition Statement">Tuition Statement</a>
              <a href="http://f2.washington.edu/fm/sfs/tuition/payment" target="_blank" data-linklabel="Make Tuition Payment">Make payment</a>
            </div>
            <div v-else>
              <span>$ 0</span>
              <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx" target="_blank" data-linklabel="Tuition Statement">Tuition Statement</a>
            </div>
          </div>
        </li>
        <!-- If there is credit on account -->
        <li v-else-if="tuition.tuition_accbalance < 0">
          <div>
	          <h4>Account Credit<br><span>Student Fiscal Services</span></h4>
	           <div>
	            <span>+${{Math.abs(tuition.tuition_accbalance).toFixed(2)}} CR</span>
	            <span>No payment needed<br></span>
	            <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx" target="_blank" data-linklabel="Tuition Statement">Tuition Statement</a>
	          </div>
	        </div>
        </li>
        <!-- If there is a PCE balance -->
        <li v-if="tuition.pce_accbalance > 0">
          <div>
            <h4>Amount Due<br><span>PCE-Continuum College</span></h4>
					  <div>
              <span>${{tuition.pce_accbalance.toFixed(2)}}</span>
              <a href="http://portal.continuum.uw.edu" target="_blank" data-linklabel="PCE Payment portal">Make payment</a>
            </div>
          </div>
        </li>
        <!-- If there is no PCE balance, either not pce or paid off -->
        <li v-else-if="isC2">
          <div>
            <h4>Amount Due<br><span>PCE-Continuum College</span></h4>
					  <div>
              <span>$ 0</span>
              <a href="http://portal.continuum.uw.edu" target="_blank" data-linklabel="Account Statement">Account Statement</a>
            </div>
          </div>
        </li>
      </ul>

    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapActions, mapState} from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      isStudent: (state) => state.user.affiliations.student,
      isGrad: (state) => state.user.affiliations.grad,
      isC2: (state) => state.user.affiliations.grad_c2 || state.user.affiliations.undergrad_c2,
      isPCE: (state) => state.user.affiliations.pce,
      tuition: (state) => state.tuition.value,
      notices: (state) => state.notices.value,
      
    }),
    ...mapGetters('tuition', {
      isReadyTuition: 'isReady',
      isErroredTuition: 'isErrored',
      statusCodeTuition: 'statusCode',
    }),
    ...mapGetters('notices', {
      isReadyNotices: 'isReady',
      isErroredNotices: 'isErrored',
      statusCodeNotices: 'statusCode',
    }),
    showError() {
      return (
        this.statusCodeNotices != 404 && this.statusCodeTuition != 404
      );
    },
  },
  created() {
    if (this.isStudent) {
      this.fetchNotices();
      this.fetchTuition();
    }
  },
  methods: {
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('tuition', {
      fetchTuition: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
