<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Husky Card</h2>
    </template>

    <template #card-body>
      <ul class="list-unstyled">
        <li v-if="hfs.student_husky_card" class="mb-1">
          <uw-card-status>
            <template #status-label>Student Husky Account</template>
            <template #status-value>${{ hfs.student_husky_card.balance.toFixed(2) }}</template>
            <template #status-content>
              <div v-if="hfs.student_husky_card.last_updated" class="myuw-text-sm text-muted">
                Last transaction: {{ hfs.student_husky_card.last_updated }}
              </div>
            </template>
          </uw-card-status>
        </li>
        <li v-if="hfs.employee_husky_card" class="mb-1">
          <uw-card-status>
            <template #status-label>Employee Husky Account</template>
            <template #status-value>${{ hfs.employee_husky_card.balance.toFixed(2) }}</template>
            <template #status-content>
              <div v-if="hfs.employee_husky_card.last_updated" class="myuw-text-sm text-muted">
                Last transaction: {{ hfs.employee_husky_card.last_updated }}
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

      <div class="text-end">
        <uw-link-button v-if="hasActionUrl" :href="getActionUrl">
          Manage Husky account
        </uw-link-button>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your Husky card balance right now. In the meantime, if
      you want to add funds, try the
      <a
        v-out="'Husky Card account summary'"
        href="https://hfs.uw.edu/olco/Secure/AccountSummary.aspx"
      >UW HFS</a> page.
    </template>
  </uw-card>
</template>
<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardStatus from '../_templates/card-status.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-status': CardStatus,
    'uw-link-button': LinkButton,
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
      student: (state) => state.user.affiliations.student,
      employee: (state) => state.user.affiliations.employee,
      past_stud: (state) => state.user.affiliations.past_stud,
      past_employee: (state) => state.user.affiliations.past_employee,
    }),
    showCard: function () {
      return (
        (this.student || this.past_stud || this.employee || this.past_employee) &&
        (!this.isReady || this.hfs.student_husky_card || this.hfs.employee_husky_card)
      );
    },
    showError: function () {
      return this.statusCode !== 404;
    },
    hasActionUrl: function () {
      return (
        (this.hfs.student_husky_card && this.hfs.student_husky_card.add_funds_url) ||
        (this.hfs.employee_husky_card && this.hfs.employee_husky_card.add_funds_url)
      );
    },
    getActionUrl: function () {
      return (this.hfs.student_husky_card
        ? this.hfs.student_husky_card.add_funds_url
        : this.hfs.employee_husky_card.add_funds_url);
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
