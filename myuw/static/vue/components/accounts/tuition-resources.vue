<template>
  <div>
    <h4>
      Related
    </h4>
    <ul>
      <li v-if="is_C2">
        <a href="https://degreereg.uw.edu/payment-procedures" target="_blank">Paying PCE-Continuum College</a>
      </li>
      <li>
        <a :href="finAidScholarshipsLink" target="_blank">Financial Aid and Scholarships</a>
      </li>
      <li v-if="is_grad">
        <a href="http://www.lib.washington.edu/commons/services/gfis" target="_blank">Graduate Funding Information Service (GFIS)</a>
      </li>
      <li v-if="!is_C2">
        <a href="http://f2.washington.edu/fm/sfs/tuition" target="_blank">About Tuition</a>
      </li>
      <li>
        <a href="http://f2.washington.edu/fm/sfs/tax" target="_blank">Student Tax Information</a>
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
      is_C2: (state) => state.user.affiliations.grad_c2 || state.user.affiliations.undergrad_c2,
      is_bothell: (state) => state.user.affiliations.bothell,
      is_tacoma: (state) => state.user.affiliations.tacoma,
    }),
  },
  methods: {
    finAidScholarshipsLink: function() {
      if (this.affiliations.is_tacoma) {
        return "http://www.tacoma.uw.edu/uwt/financial-aid";
      } else if (this.affiliations.is_bothell) {
        return "https://www.uwb.edu/financialaid";
      } else if (this.affiliations.is_C2) {
        return "https://www.washington.edu/financialaid/getting-started/eligibility/fee-based-programs/";
      } else {
        return "http://www.washington.edu/students/osfa/";
      }
    }
  },
};
</script>

<style lang="scss" scoped>
</style>
