<template>
  <uw-card v-if="showCard" :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">ID Card</h2>
    </template>

    <template #card-body>
      <ul class="list-unstyled">
        <li v-if="idcard.student_eligible" class="mb-1">
          <uw-card-status>
            <template #status-label>Your Student ID</template>
            <template #status-value>is eligible</template>
            <template #status-content>
              <div class="myuw-text-sm text-muted">
                ......
              </div>
            </template>
          </uw-card-status>
        </li>
        <li v-if="idcard.employee_eligible" class="mb-1">
          <uw-card-status>
            <template #status-label>Your Employee ID</template>
            <template #status-value>is eligible</template>
            <template #status-content>
              <div class="myuw-text-sm text-muted">
                ......
              </div>
            </template>
          </uw-card-status>
        </li>
        <li v-if="idcard.retiree_eligible" class="mb-1">
          <uw-card-status>
            <template #status-label>Your Retiree ID</template>
            <template #status-value>is eligible</template>
            <template #status-content>
              <div class="myuw-text-sm text-muted">
                ......
              </div>
            </template>
          </uw-card-status>
        </li>
      </ul>

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
    'uw-link-button': LinkButton,
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
      past_stud: (state) => state.user.affiliations.past_stud,
      past_employee: (state) => state.user.affiliations.past_employee,
    }),
    showCard() {
      return (
        (this.student || this.past_stud || this.employee || this.past_employee) &&
        (!this.isReady || this.idcard)
      );
    },
    showError() {
      return this.statusCode !== 404;
    },
  },
  created() {
    if (this.student || this.past_stud || this.employee || this.past_employee) this.fetchIDcard();
  },
  methods: {
    ...mapActions('idcardelig', {
      fetchIDcard: 'fetch',
    }),
  },
};
</script>
