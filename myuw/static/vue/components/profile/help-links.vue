<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <h3 class="h5">
        Related Help
      </h3>
      <ul class="list-unstyled myuw-text-md mb-4">
        <li v-if="isBothell" class="mb-1">
          <a href="https://www.uwb.edu/facility/mail-services">Mailing Services</a>
        </li>
        <li v-else-if="!isTacoma" class="mb-1">
          <a href="http://www.washington.edu/about/addressing-letters-to-the-uw/">Addressing Letters to the UW</a>
        </li>
        <li class="mb-1">
          <a :href="prefNameLink">Preferred Names</a>
        </li>
        <template v-if="student || studEmployee">
          <li v-if="isTacoma" class="mb-1">
            <a href="http://www.tacoma.uw.edu/sites/default/files/sections/Registrar/Change-Student-Name.pdf">Change Your Legal Name</a>
          </li>
          <li v-else-if="isBothell" class="mb-1">
            <a href="https://www.uwb.edu/registration/policies/name-change">Name Change Policy</a>
          </li>
          <template v-else>
            <li class="mb-1">
              <a href="https://registrar.washington.edu/enrollment-and-records/name-change-policy/">Change Your Legal Name</a>
            </li>
            <li class="mb-1">
              <a href="https://depts.washington.edu/qcenter/wordpress/changing-your-name-in-the-uw-student-database/">Changing Your Name and Gender</a>
            </li>
          </template>
        </template>
        <li v-if="employee || studEmployee" class="mb-1">
          <a href="http://hr.uw.edu/benefits/life-events/change-your-address-name-gender-citizenship-or-birth-date/">Change Your Personal Information</a>
        </li>
        <li v-if="student" class="mb-1">
          <a href="https://registrar.washington.edu/enrollment-and-degree-verification/">Self-Service Enrollment Verification</a>
        </li>
      </ul>
    </template>
  </uw-panel>
</template>

<script>
import { mapState } from 'vuex';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
  },
  computed: {
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      studEmployee: (state) => state.user.affiliations.stud_employee,
      student: (state) => state.user.affiliations.student,
      isTacoma: (state) => state.user.affiliations.tacoma,
      isBothell: (state) => state.user.affiliations.bothell,
    }),
    prefNameLink() {
      return (this.isTacoma
      ? 'https://www.tacoma.uw.edu/office-registrar/preferred-names'
      : 'https://registrar.washington.edu/students/preferred-names/');
    },
  },
};
</script>
