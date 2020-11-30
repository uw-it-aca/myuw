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

      <div>
        <p v-if="!isC2Grad">
          <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/release.aspx" target="_blank">Give access to your tuition account and financial aid information</a> to parents or other third parties.
        </p>
        <p v-for="(msg, i) in pceTuitionDup" :key="i">
          {{ msg.notice_content }}
        </p>
      </div>

      <uw-fin-aid
        v-if="finAidNotices && finAidNotices.length"
        :fin-aid-notices="finAidNotices"
      >
        <template #status>
          <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/finaidstatus.aspx" target="_blank" data-linklabel="Financial Aid Status">Financial Aid Status</a>
        </template>
      </uw-fin-aid>

      <uw-tuition-resources />
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. In the meantime, try the
      <a v-if="!isPCE" href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx" data-linklabel="Tuition Statement" target="_blank">Tuition Statement page</a>
      <a v-else href="https://portal.continuum.uw.edu" data-linklabel="PCE Tuition portal" target="_blank">PCE Tuition portal</a>.
      <uw-tuition-resources />
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapActions, mapState} from 'vuex';
import Card from '../_templates/card.vue';
import FinAidComponent from '../home/registration/finaid.vue';
import TuitionResources from './tuition-resources.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-fin-aid': FinAidComponent,
    'uw-tuition-resources': TuitionResources,
  },
  computed: {
    ...mapState({
      isStudent: (state) => state.user.affiliations.student,
      isC2Grad: (state) => state.user.affiliations.grad_c2,
      isC2: (state) => state.user.affiliations.grad_c2 || state.user.affiliations.undergrad_c2,
      isPCE: (state) => state.user.affiliations.pce,
      tuition: (state) => state.tuition.value,
      notices: (state) => state.notices.value,
      finAidNotices: (state) => { 
        return state.notices.value.filter(
          (notice) => notice.location_tags.includes('tuition_aidhold_title') ||
          notice.location_tags.includes('tuition_missingdocs_title') ||
          notice.location_tags.includes('tuition_loanpromissory_title') ||
          notice.location_tags.includes('tuition_loancounseling_title') ||
          notice.location_tags.includes('tuition_acceptreject_title') ||
          notice.location_tags.includes('tuition_disbursedateA_title') ||
          notice.location_tags.includes('tuition_disbursedateB_title') ||
          notice.location_tags.includes('tuition_direct_deposit_title') ||
          notice.location_tags.includes('tuition_aid_prioritydate_title') ||
          notice.location_tags.includes('tuition_aid_reminder_title') ||
          notice.location_tags.includes('tuition_summeraid_date_title') ||
          notice.location_tags.includes('tuition_summeraid_avail_title')
        );
      },
      pceTuitionDup: (state) => {
        return state.notices.value.filter(
          (notice) => notice.location_tags.includes('pce_tuition_dup')
        );
      },
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
