<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Husky Card Eligibility</h2>
    </template>

    <template #card-body>
      <ul class="list-unstyled">
        <li v-if="idcard.not_eligible" class="mb-1">
          <uw-card-status>
            <template #status-label>Status</template>
            <template #status-value>Not Eligible</template>
            <template #status-content>
              <div v-if="hfs.student_husky_card.last_updated" class="myuw-text-sm text-muted">
                No access into buildings, no UPASS membership, no parking permit, etc.
              </div>
            </template>
          </uw-card-status>
        </li>
        <li v-else class="mb-1">
          <uw-card-status>
            <template #status-label>Status</template>
            <template #status-value>
              <ul class="list-unstyled">
                <li v-if="idcard.student_eligible" class="mb-1">Student Eligible</li>
                <li v-if="idcard.retiree_eligible" class="mb-1">Retiree Eligible</li>
                <li v-if="idcard.employee_eligible" class="mb-1">Employee Eligible</li>
              </ul>
            </template>
          </uw-card-status>
        </li>
      </ul>
      <div class="myuw-text-sm text-muted">
        <a href="https://hfs.uw.edu/Husky-Card-Services">About Husky Card</a>
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your ID card right now. In the meantime,
      check out
      <a
        v-out="'idcard'"
        href="https://hfs.uw.edu/Husky-Card-Services/Husky-Card/ID-Center-Locations"
      >the ID center</a>.
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
    ...mapState('idcardelig', {
      idcard: (state) => state.value,
    }),
    ...mapGetters('idcardelig', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      statusCode: 'statusCode',
    }),
    ...mapState({
      student: (state) => state.user.affiliations.student,
      employee: (state) => state.user.affiliations.all_employee,
      retiree: (state) => state.user.affiliations.retiree,
    }),
    showCard() {
      return (
        (this.student || this.employee || this.retiree) &&
        (!this.isReady || this.idcard)
      );
    },
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student || this.employee || this.retiree) this.fetchIDcard();
  },
  methods: {
    ...mapActions('idcardelig', {
      fetchIDcard: 'fetch',
    }),
  },
};
</script>
