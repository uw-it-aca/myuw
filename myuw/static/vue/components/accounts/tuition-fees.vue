<template>
  <uw-card
    v-if="isStudent"
    :loaded="isReadyNotices && isReadyTuition"
    :errored="isErroredNotices || isErroredTuition"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Tuition &amp; Fees</h2>
    </template>
    <template #card-body>
      <div style="text-align: center">
        <b-alert
          v-if="tuitionDate.diff === 0 && tuition.tuition_accbalance > 0"
          show
          variant="danger"
          class="text-danger"
        >
          <font-awesome-icon :icon="faExclamationTriangle" /> Tuition and fees are due
          today.
        </b-alert>
        <b-alert
          v-if="tuitionDate.diff < 0 && tuition.tuition_accbalance > 0"
          show
          variant="danger"
          class="text-danger"
        >
          <font-awesome-icon :icon="faExclamationTriangle" />
          You have a balance that may be past due. See your statement for details.
        </b-alert>
      </div>

      <ul class="list-unstyled">
        <!-- If there is some or no tuition due -->
        <li v-if="tuition.tuition_accbalance >= 0">
          <uw-card-status>
            <template #status-label>Amount Due</template>
            <template v-if="tuition.tuition_accbalance > 0" #status-value>
              <span class="text-danger">${{ tuition.tuition_accbalance.toFixed(2) }}</span>
            </template>
            <template v-else #status-value>$ 0</template>
            <template #status-content>
              <div class="d-flex mb-2 myuw-text-md">
                <div class="flex-fill w-50">Student Fiscal Services</div>
                <div class="flex-fill w-50 text-right">
                  <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx">
                    Tuition Statement
                    </a>
                </div>
              </div>
              <div class="text-right">
                <uw-link-button
                  v-out="'Make tuition payment'"
                  href="http://f2.washington.edu/fm/sfs/tuition/payment"
                >
                  Make payment
                </uw-link-button>
              </div>
            </template>
          </uw-card-status>
        </li>
        <!-- If there is credit on account -->
        <li v-else-if="tuition.tuition_accbalance < 0">
          <div class="d-flex">
            <div>
              <h3 class="h6 text-dark font-weight-bold">
                Account Credit<br />
                <span class="myuw-text-md">Student Fiscal Services</span>
              </h3>
            </div>
            <div>
              <span class="h6 text-dark font-weight-bold"
                >+${{ Math.abs(tuition.tuition_accbalance).toFixed(2) }} CR</span
              >
              <span>No payment needed</span><br />
              <a
                href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
                class="myuw-text-md"
              >Tuition Statement</a>
            </div>
          </div>
        </li>
        <!-- If there is a PCE balance -->
        <li v-if="tuition.pce_accbalance > 0">
          <uw-card-status>
            <template #status-label>Amount Due</template>
            <template #status-value>
              <span class="text-danger">${{ tuition.pce_accbalance.toFixed(2) }}</span>
            </template>
            <template #status-content>
              <div class="myuw-text-md">PCE-Continuum College</div>
              <div class="text-right">
                <uw-link-button
                  v-out="'Make Continuum College tuition payment'"
                  href="http://portal.continuum.uw.edu"
                 >
                  Make payment
                </uw-link-button>
              </div>
            </template>
          </uw-card-status>
        </li>
        <!-- If there is no PCE balance, either not pce or paid off -->
        <li v-else-if="isC2">
          <uw-card-status>
            <template #status-label>Amount Due</template>
            <template #status-value>$ 0</template>
            <template #status-content>
              <span class="myuw-text-md">PCE-Continuum College</span>
              <a v-out="'Continuum College Account Statement'"
                href="http://portal.continuum.uw.edu"
                class="myuw-text-md"
              >Account Statement</a>
            </template>
          </uw-card-status>
        </li>

        <li v-if="tuitionDate.formatted && tuitionDate.diff >= 0">
          <uw-card-status>
            <template #status-label>Payment Due</template>
            <template #status-value>{{ tuitionDate.formatted }}</template>
            <template #status-content>
              <div class="myuw-text-md text-body text-right">
                <span v-if="tuitionDate.diff === 0">Today</span>
                <span v-else-if="tuitionDate.diff === 1">Tomorrow</span>
                <span v-else>in {{ tuitionDate.diff }} days</span>
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

      <div class="myuw-text-md">
        <p v-if="!isC2Grad">
          <a v-out="'Give Tuition Account Access'"
            href="https://sdb.admin.uw.edu/sisStudents/uwnetid/release.aspx"
          >Give access to your tuition account and financial aid information
          </a>
          to parents or other third parties.
        </p>
        <p v-for="(msg, i) in pceTuitionDup" :key="i">
          {{ msg.notice_content }}
        </p>
      </div>

      <uw-fin-aid :fin-aid-notices="finAidNotices">
        <template #status>
          <ul class="list-unstyled myuw-text-md mb-1">
            <li>
              <a
                href="https://sdb.admin.uw.edu/sisStudents/uwnetid/finaidstatus.aspx"
                class="myuw-text-md"
              >Financial Aid Status</a>
            </li>
          </ul>
        </template>
      </uw-fin-aid>

      <uw-tuition-resources />
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. In the meantime, try the
      <a v-if="!isPCE"
        v-out="'Tuition Statement'"
        href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
      >Tuition Statement page</a>
      <a v-else
        v-out="'Continuum College Tuition portal'"
        href="https://portal.continuum.uw.edu"
      >PCE Tuition portal</a>.
    </template>
    <template #card-error-extra>
      <uw-tuition-resources />
    </template>
  </uw-card>
</template>

<script>
import {
  faExclamationTriangle,
} from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapActions, mapState } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';
import LinkButton from '../_templates/link-button.vue';
import FinAidComponent from '../_common/finaid.vue';
import TuitionResources from './tuition-resources.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-link-button': LinkButton,
    'uw-fin-aid': FinAidComponent,
    'uw-tuition-resources': TuitionResources,
  },
  data: function () {
    return {
      finAidTags: [
        'tuition_aidhold_title',
        'tuition_missingdocs_title',
        'tuition_loanpromissory_title',
        'tuition_loancounseling_title',
        'tuition_acceptreject_title',
        'tuition_disbursedateA_title',
        'tuition_disbursedateB_title',
        'tuition_direct_deposit_title',
        'tuition_aid_prioritydate_title',
        'tuition_aid_reminder_title',
        'tuition_summeraid_date_title',
        'tuition_summeraid_avail_title',
      ],
      faExclamationTriangle,
    };
  },
  computed: {
    ...mapState({
      isStudent: (state) => state.user.affiliations.student,
      isC2Grad: (state) => state.user.affiliations.grad_c2,
      isC2: (state) => {
        return state.user.affiliations.grad_c2 || state.user.affiliations.undergrad_c2;
      },
      isPCE: (state) => state.user.affiliations.pce,
      tuition: (state) => state.tuition.value,
      notices: (state) => state.notices.value,
      pceTuitionDup: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('pce_tuition_dup')
        );
      },
      tuitionDueNotice: (state) => {
        return state.notices.value.filter((notice) =>
          notice.location_tags.includes('tuition_due_date')
        )[0];
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
      return this.statusCodeNotices != 404 && this.statusCodeTuition != 404;
    },
    finAidNotices: function () {
      const notices = [];
      for (let i = 0; i < this.finAidTags.length; i++) {
        const notice = this.notices.filter((notice) => {
          return notice.location_tags.includes(this.finAidTags[i]);
        })[0];
        if (notice !== undefined) {
          notices.push(notice);
        }
      }
      return notices;
    },
    tuitionDate() {
      // from notice
      const now = this.nowDatetime();
      const result = {};
      if (this.tuitionDueNotice && this.tuitionDueNotice.date) {
        result.diff = Math.ceil(this.tuitionDueNotice.date.diff(now, 'day', true));
        result.formatted = this.tuitionDueNotice.formattedDate;
      }
      return result;
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
