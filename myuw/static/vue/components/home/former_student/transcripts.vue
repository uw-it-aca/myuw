<template>
  <uw-card
    v-if="pastStudent"
    :loaded="true"
  >
    <template #card-heading>
      <h3 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Order Transcripts
      </h3>
    </template>
    <template #card-body>
      <p class="myuw-text-md">
        For those who have graduated in 1983 or later:
      </p>
      <ul class="list-unstyled myuw-text-md mb-4">
        <li class="mb-1">
          <a href="https://apps.registrar.washington.edu/credential_solutions_authentication/public/ce.php"
            target="_blank" data-linklabel="Official Transcript">Order Official Transcripts</a>
        </li>
        <li class="mb-1">
          <a href="https://sdb.admin.uw.edu/students/uwnetid/unofficial.asp" target="_blank" data-linklabel="Unofficial Transcript">View Unofficial Transcript</a>
        </li>
      </ul>
      <h4 class="h6 text-dark-beige myuw-font-roboto">
        Contact the Registrar
      </h4>
      <p class="myuw-text-md">
        For transcripts from 1982 and before, contact
        the Office of the University Registrar.
        The Registrar provides administrative
        services to students, faculty, and staff.
      </p>
      <ul class="list-unstyled myuw-text-md mb-0">
        <li class="mb-1">
          <a href="https://registrar.washington.edu" target="_blank" data-linklabel="UW Registrar">Contact the UW Registrar</a>
        </li>
        <li class="mb-1">
          <a href="https://www.uwb.edu/registration" target="_blank" data-linklabel="UW Bothell Registrar">Contact the UW Bothell Registrar</a>
        </li>
        <li class="mb-1">
          <a href="https://www.tacoma.uw.edu/office-registrar/office-registrar" target="_blank" data-linklabel="UW Tacoma Registrar">Contact the UW Tacoma Registrar</a>
        </li>
      </ul>
    </template>
  </uw-card>
</template>

<script>
import {mapState} from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      pastStudent: (state) => state.user.affiliations.past_stud,
    }),
  },
};
</script>

<style lang="scss" scoped>
</style>
