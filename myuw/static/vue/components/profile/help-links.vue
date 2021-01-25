<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <h4>
        Related Help
      </h4>
      <ul>
        <li v-if="isBothell">
          <a href="https://www.uwb.edu/facility/mail-services">Mailing Services</a>
        </li>
        <li v-else-if="!isTacoma">
          <a href="http://www.washington.edu/about/addressing-letters-to-the-uw/">Addressing Letters to the UW</a>
        </li>
        <li v-if="isTacoma">
          <a href="https://www.tacoma.uw.edu/office-registrar/preferred-names">Preferred Names</a>
        </li>
        <li>
          <a :href="isTacoma ? prefNameLinkTac : prefNameLink">Preferred Names</a>
        </li>
        <template v-if="student">
          <li v-if="isTacoma">
            <a href="http://www.tacoma.uw.edu/sites/default/files/sections/Registrar/Change-Student-Name.pdf">Change Your Legal Name</a>
          </li>
          <li v-else-if="isBothell">
            <a href="https://www.uwb.edu/registration/policies/name-change" class="student_legal_name">Name Change Policy</a>
          </li>
          <template v-else>
            <li>
              <a href="https://registrar.washington.edu/enrollment-and-records/name-change-policy/" class="student_legal_name">Change Your Legal Name</a>
            </li>
            <li>
              <a href="https://depts.washington.edu/qcenter/wordpress/changing-your-name-in-the-uw-student-database/">Changing Your Name and Gender</a>
            </li>
          </template>
        </template>
        <li v-if="employee">
          <a href="http://hr.uw.edu/benefits/life-events/change-your-address-name-gender-citizenship-or-birth-date/" class="employee_work_info">Change Your Personal Information</a>
        </li>
        <li v-if="student">
          <a href="https://registrar.washington.edu/enrollment-and-degree-verification/">Self-Service Enrollment Verification</a>
        </li>
      </ul>
    </template>
  </uw-panel>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
  },
  data: function() {
    return {
      prefNameLinkTac: 'https://www.tacoma.uw.edu/office-registrar/preferred-names',
      prefNameLink: 'https://registrar.washington.edu/students/preferred-names/',
    };
  },
  computed: {
    ...mapState({
      employee: (state) => state.user.affiliations.employee,
      student: (state) => state.user.affiliations.student,
      isTacoma: (state) => state.user.affiliations.tacoma,
      isBothell: (state) => state.user.affiliations.bothell,
    }),
  },
};
</script>
