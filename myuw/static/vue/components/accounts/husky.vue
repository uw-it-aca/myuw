<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Husky Card</h3>
    </template>

    <template #card-body>
      <ul class="list-unstyled">
        <li>
          <uw-card-status v-if="hfs.student_husky_card">
            <template #status-label>Student Husky Account</template>
            <template #status-value>${{ hfs.student_husky_card.balance.toFixed(2) }}</template>
            <template #status-content>
              <div v-if="hfs.student_husky_card.last_updated" class="myuw-text-sm text-muted">
                Last transaction: {{ hfs.student_husky_card.last_updated }}
              </div>
            </template>
          </uw-card-status>
        </li>
        <li>
          <uw-card-status v-if="hfs.employee_husky_card">
            <template #status-label>Employee Husky Account</template>
            <template #status-value>${{ hfs.employee_husky_card.balance.toFixed(2) }}</template>
            <template #status-content>
              <div v-if="hfs.student_husky_card.last_updated" class="myuw-text-sm text-muted">
                Last transaction: {{ hfs.employee_husky_card.last_updated }}
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

      <div class="text-right">
        <a
          v-if="hasActionUrl"
          :href="getActionUrl"
          target="_blank"
          aria-label="Manage Husky account"
          class="btn btn-outline-beige text-dark myuw-text-md"
        >
          Manage account
        </a>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your Husky card balance right now. In the meantime, if
      you want to add funds, try the
      <a
        href="https://hfs.uw.edu/olco/Secure/AccountSummary.aspx"
        data-linklabel="Husky card account"
        target="_blank"
      >
        UW HFS page </a
      >.
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
      if (this.hfs.student_husky_card) {
        return this.hfs.student_husky_card.add_funds_url;
      }
      return this.hfs.employee_husky_card.add_funds_url;
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
