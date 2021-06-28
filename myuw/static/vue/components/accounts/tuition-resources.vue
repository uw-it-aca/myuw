<template>
  <div>
    <h3 class="h6 text-dark-beige myuw-font-encode-sans">
      Related
    </h3>
    <ul class="list-unstyled myuw-text-md">
      <li v-if="is_C2" class="mb-1">
        <a href="https://degreereg.uw.edu/payment-procedures">
          Paying PCE-Continuum College
        </a>
      </li>
      <li class="mb-1">
        <a :href="finAidScholarshipsLink">
          Financial Aid and Scholarships
        </a>
      </li>
      <li v-if="is_grad" class="mb-1">
        <a href="http://www.lib.washington.edu/commons/services/gfis">
          Graduate Funding Information Service (GFIS)
        </a>
      </li>
      <li v-if="!is_C2" class="mb-1">
        <a href="http://f2.washington.edu/fm/sfs/tuition">About Tuition</a>
      </li>
      <li class="mb-1">
        <a href="http://f2.washington.edu/fm/sfs/tax">Student Tax Information</a>
      </li>
    </ul>
  </div>
</template>

<script>
import {mapState} from 'vuex';
export default {
  computed: {
    ...mapState({
      is_grad: (state) => state.user.affiliations.grad,
      is_C2: (state) => {
        return state.user.affiliations.grad_c2 ||
               state.user.affiliations.undergrad_c2;
      },
      is_bothell: (state) => state.user.affiliations.bothell,
      is_tacoma: (state) => state.user.affiliations.tacoma,
    }),
    finAidScholarshipsLink() {
      if (this.is_tacoma) {
        return 'http://www.tacoma.uw.edu/uwt/financial-aid';
      } else if (this.is_bothell) {
        return 'https://www.uwb.edu/financialaid';
      } else if (this.is_C2) {
        return 'https://www.washington.edu/financialaid/getting-started/eligibility/fee-based-programs/';
      } else {
        return 'http://www.washington.edu/students/osfa/';
      }
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
