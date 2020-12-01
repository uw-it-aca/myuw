<template>
  <uw-card
    v-if="showCard"
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h3>
        Husky Card
      </h3>
    </template>
    <template #card-error>
      <p>
        <i class="fa fa-exclamation-triangle" />
        An error occurred and MyUW cannot load your Husky card balance
        right now. In the meantime, if you want to add funds, try the
        <a href="https://hfs.uw.edu/olco/Secure/AccountSummary.aspx"
           data-linklabel="Husky card account"
           target="_blank"
        >
          UW HFS page
        </a>.
      </p>
    </template>
    <template #card-body>
      <div v-if="hfs.student_husky_card">
        <h4>
          Student Husky Account
        </h4>
        <div>
          <span>${{ hfs.student_husky_card.balance.toFixed(2) }}</span>
        </div>
        <div v-if="hfs.student_husky_card.last_updated">
          <span>
            Last transaction: {{ hfs.student_husky_card.last_updated }}
          </span>
        </div>
      </div>

      <div v-if="hfs.employee_husky_card">
        <h4>
          Employee Husky Account
        </h4>
        <div>
          <span>${{ hfs.employee_husky_card.balance.toFixed(2) }}</span>
        </div>
        <div v-if="hfs.employee_husky_card.last_updated">
          <span>
            Last transaction: {{ hfs.employee_husky_card.last_updated }}
          </span>
        </div>
      </div>
      <div>
        <a v-if="hfs.student_husky_card"
           :href="hfs.student_husky_card.add_funds_url"
           target="_blank"
           aria-label="Manage Husky account"
        >
          Manage account
        </a>
        <a v-else
           :href="hfs.employee_husky_card.add_funds_url"
           target="_blank"
           aria-label="Manage Husky account"
        >
          Manage account
        </a>
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
      student: (state) => state.user.affiliations.student,
      employee: (state) => state.user.affiliations.employee,
      past_stud: (state) => state.user.affiliations.past_stud,
      past_employee: (state) => state.user.affiliations.past_employee,
    }),
    showCard: function() {
      return !this.isReady ||
        (this.student || this.past_stud ||
        this.employee || this.past_employee) && this.hfs &&
        (this.hfs.student_husky_card || this.hfs.employee_husky_card);
    },
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


