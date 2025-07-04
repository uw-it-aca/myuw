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
      <div>
        <!--<div v-if="hasIacData" role="alert" class="alert alert-warning myuw-text-md">
          <font-awesome-icon :icon="faExclamationTriangle" />
          <strong>Digital material fees are not included in tuition</strong>. They must be paid
          separately below under "UW Day One Access Fees."
        </div>-->
        <div
          v-if="hasTuitionDate && tuitionDateFromNow === 'Today' && tuiBalance > 0"
          class="alert alert-danger text-danger" style="text-align: center"
          role="alert"
        >
          <font-awesome-icon :icon="faExclamationTriangle" /> Tuition and fees are due today.
        </div>
        <div
          v-if="hasTuitionDate && daysDiffTuitionDueDate < 0 && tuiBalance > 0"
          class="alert alert-danger text-danger myuw-text-md"
          role="alert"
        >
          <font-awesome-icon :icon="faExclamationTriangle" />
          You have a balance that may be past due. See your statement for details.
        </div>
      </div>

      <ul class="list-unstyled">
        <!-- If there is some or no tuition due -->
        <li v-if="tuiBalance >= 0">
          <uw-card-status>
            <template #status-label>Student Fiscal Services (SFS)</template>
            <template v-if="tuiBalance > 0" #status-value>
              <span class="text-danger">${{ tuiBalance.toFixed(2) }}</span>
            </template>
            <template v-else #status-value>$ 0</template>
            <template #status-content>
              <div class="d-flex mb-1 myuw-text-md row">
                <div class="col">Amount Due</div>
                <div class="col text-end">
                  <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
                    >Tuition Statement</a
                  >
                </div>
              </div>
              <div v-if="tuiBalance != 0" class="text-end">
                <uw-link-button
                  v-out="'Pay SFS tuition'"
                  class=""
                  style="width: 10rem;"
                  href="https://f2.washington.edu/fm/sfs/tuition/payment"
                  >Pay SFS tuition</uw-link-button
                >
              </div>
            </template>
          </uw-card-status>
        </li>
        <!-- If there is credit on account -->
        <li v-else-if="tuiBalance < 0">
          <uw-card-status>
            <template #status-label>Student Fiscal Services (SFS)</template>
            <template #status-value> +${{ Math.abs(tuiBalance).toFixed(2) }} CR </template>
            <template #status-content>
              <div class="d-flex mb-2 myuw-text-md row">
                <div class="col">Account Credit</div>
                <div class="col text-end">
                  No payment needed<br>
                  <a href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
                    >Tuition Statement</a
                  >
                </div>
              </div>
            </template>
          </uw-card-status>
        </li>
        <!-- If there is a PCE balance -->
        <li v-if="pceBalance > 0">
          <uw-card-status>
            <template #status-label>PCE - Continuum College</template>
            <template #status-value>
              <span class="text-danger">${{ pceBalance.toFixed(2) }}</span>
            </template>
            <template #status-content>
              <div class="d-flex mb-2 myuw-text-md row">
                <div class="col">Amount Due</div>
                <div class="text-end col">
                  <uw-link-button
                    v-out="'Pay PCE tuition'"
                    style="width: 10rem;"
                    href="https://portal.continuum.uw.edu"
                    >Pay PCE tuition</uw-link-button
                  >
                </div>
              </div>
            </template>
          </uw-card-status>
        </li>
        <!-- If there is no PCE balance, either not pce or paid off -->
        <li v-else-if="isC2">
          <uw-card-status>
            <template #status-label>PCE-Continuum College</template>
            <template #status-value>$ 0</template>
            <template #status-content>
              <div class="d-flex mb-2 myuw-text-md">
                <div class="flex-fill w-50">Amount Due</div>
                <div class="flex-fill w-50 text-end">
                  <a
                    v-out="'Continuum College Account Statement'"
                    href="https://portal.continuum.uw.edu"
                    class="myuw-text-md"
                    >Account Statement</a
                  >
                </div>
              </div>
            </template>
          </uw-card-status>
        </li>

        <li v-if="hasTuitionDate">
          <uw-card-status>
            <template #status-label>Payment Due</template>
            <template #status-value>
              <uw-formatted-date :due-date="tuitionDate"></uw-formatted-date>
            </template>
            <template #status-content>
              <div class="myuw-text-md text-body text-end">
                {{ tuitionDateFromNow }}
              </div>
            </template>
          </uw-card-status>
        </li>

        <li v-if="hasIacData">
          <h3 class="h6 text-dark-beige myuw-font-encode-sans mt-4">UW Day One Access Fees</h3>
          <div class="alert alert-warning myuw-text-md" role="alert">
            <p>
              One or more of your enrolled courses provides you access to
              <a :href="textbooksUrl">required digital materials</a>, in Canvas, on or before the
              first day of class.
            </p>
            <p class="mb-0">
              <strong
                >To maintain access to these materials at Day One Access pricing, you must pay for
                these materials</strong
              >.
              <a href="https://www.ubookstore.com/day-one-access-faq"
                >About the Day One Access Program</a
              >.
            </p>
          </div>
          <div v-if="dayOneAccessOverDue" role="alert" class="alert alert-danger myuw-text-md">
            <strong>The payment deadline has passed.</strong> To learn about your options, please
            email <a href="mailto:dayoneaccess@ubookstore.com">dayoneaccess@ubookstore.com</a>.
          </div>
          <uw-card-status v-else>
            <template #status-label>University Book Store</template>
            <template v-if="iacData.balance > 0" #status-value>
              <span class="text-danger">${{ iacData.balance.toFixed(2) }}</span>
            </template>
            <template v-else #status-value>$ 0</template>

            <template v-if="iacData.balance > 0" #status-content>
              <div class="d-flex mb-2 myuw-text-md row">
                <div class="col">Amount Due</div>
                <div class="text-end col">
                  <uw-link-button
                    v-out="'Pay book store tuition'"
                    style="width: 10rem;"
                    :href="iacData.bookstore_checkout_url"
                    >Pay book store fees</uw-link-button
                  >
                </div>
              </div>
            </template>
          </uw-card-status>
        </li>

        <li v-if="hasIacData && iacData.balance > 0 && !dayOneAccessOverDue">
          <uw-card-status>
            <template #status-label>Payment Due</template>
            <template #status-value>
              <uw-formatted-date :due-date="iacData.payment_due_day" />
            </template>
            <template #status-content>
              <div class="myuw-text-md text-body text-end">
                {{ dayOneAccessDueDateFromNow }}
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

      <div class="myuw-text-md">
        <p v-if="!isC2Grad">
          <a
            v-out="'Give Tuition Account Access'"
            href="https://sdb.admin.uw.edu/sisStudents/uwnetid/release.aspx"
            >Give access to your tuition account and financial aid information</a
          >
          to parents or other third parties.
        </p>
        <p v-for="(msg, i) in pceTuitionDup" :key="i">
          {{ msg.notice_content }}
        </p>
      </div>

      <uw-fin-aid :fin-aid-notices="finAidNotices">
        <template #status>
          <ul class="list-unstyled myuw-text-md mb-1">
            <li class="mb-1">
              <a
                href="https://sdb.admin.uw.edu/sisStudents/uwnetid/finaidstatus.aspx"
                class="myuw-text-md"
                >Financial Aid Status</a
              >
            </li>
          </ul>
        </template>
      </uw-fin-aid>

      <uw-tuition-resources />
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your information right now. In the meantime, try the
      <span v-if="!isPCE">
        <a
          v-out="'Tuition Statement'"
          href="https://sdb.admin.uw.edu/sisStudents/uwnetid/tuition.aspx"
          >Tuition Statement</a
        >
        page.
      </span>
      <span v-else>
        <a v-out="'Continuum College Tuition portal'" href="https://portal.continuum.uw.edu"
          >PCE Tuition</a
        >
        portal.
      </span>
    </template>
    <template #card-error-extra>
      <uw-tuition-resources />
    </template>
  </uw-card>
</template>

<script>
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapActions, mapState } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';
import LinkButton from '../_templates/link-button.vue';
import FinAidComponent from '../_common/finaid.vue';
import TuitionResources from './tuition-resources.vue';
import FormattedDate from '../_common/formatted-date.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-link-button': LinkButton,
    'uw-fin-aid': FinAidComponent,
    'uw-tuition-resources': TuitionResources,
    'uw-formatted-date': FormattedDate,
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
      seaStud: (state) => state.user.affiliations.seattle,
      botStud: (state) => state.user.affiliations.bothell,
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
    ...mapState('iac', {
      iacData(state) {
        return state.value;
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
    ...mapGetters('iac', {
      isIacReady: 'isReadyTagged',
      isIacErrored: 'isErroredTagged',
      statusCodeIac: 'statusCodeTagged',
    }),
    showError() {
      return (
        (this.isErroredNotices && this.statusCodeNotices != 404) ||
        (this.isErroredTuition && this.statusCodeTuition != 404)
      );
    },
    finAidNotices() {
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
    hasTuitionDate() {
      return Boolean(this.tuitionDueNotice) && Boolean(this.tuitionDueNotice.dateStr);
    },
    tuitionDate() {
      // To change due date on localdev, uncomment the line below:
      // this.tuitionDueNotice.dateStr = "2013-04-14 07:00:00+00:00";
      return this.tuitionDueNotice.dateStr;
    },
    tuitionDateFromNow() {
      return this.toFromNowDate(this.tuitionDate);
    },
    daysDiffTuitionDueDate() {
      return this.timeDeltaFrom(this.tuitionDate);
    },
    tuiBalance() {
      // regular tuition balance
      return this.tuition.tuition_accbalance;
    },
    pceBalance() {
      return this.tuition.pce_accbalance;
    },
    hasIacData() {
      // MUWM-5272
      return (this.seaStud || this.botStud) && this.iacData && this.iacData.bookstore_checkout_url;
    },
    dayOneAccessDueDateFromNow() {
      // MUWM-5272
      return this.toFromNowDate(this.iacData.payment_due_day);
    },
    dayOneAccessOverDue() {
      // MUWM-5351
      return this.hasPassed(this.iacData.payment_due_day);
    },
    textbooksUrl() {
      // MUWM-5272
      return '/textbooks/' + this.iacData.year + ',' + this.iacData.quarter;
    },
  },
  created() {
    if (this.isStudent) {
      this.fetchNotices();
      this.fetchTuition();
      if (this.seaStud || this.botStud) this.fetchIACs('current');
    }
  },
  methods: {
    ...mapActions('notices', {
      fetchNotices: 'fetch',
    }),
    ...mapActions('tuition', {
      fetchTuition: 'fetch',
    }),
    ...mapActions('iac', {
      fetchIACs: 'fetch',
    }),
  },
};
</script>

<style lang="scss" scoped></style>
