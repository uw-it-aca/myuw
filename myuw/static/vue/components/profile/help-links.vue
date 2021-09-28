<template>
  <uw-panel :loaded="true">
    <template #panel-body>
      <uw-sidelink-section
        category-title="Related Help"
        :links="linkList"
      />
    </template>
  </uw-panel>
</template>

<script>
import { mapState } from 'vuex';
import Panel from '../_templates/panel.vue';
import SidelinkSection from '../_templates/sidelink-section.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-sidelink-section': SidelinkSection,
  },
  computed: {
    ...mapState({
      employee: (state) => state.user.affiliations.all_employee,
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
    linkList() {
      return [
        this.isBothell ?
          { url: "https://www.uwb.edu/facility/mail-services", title: "Mailing Services" } : null,
        !this.isBothell && !this.isTacoma ?
          { url: "http://www.washington.edu/about/addressing-letters-to-the-uw/",
            title: "Addressing Letters to the UW"} : null,
        { url: this.prefNameLink, title: "Preferred Names"},
        (this.student || this.studEmployee) && this.isTacoma ?
          { url: "http://www.tacoma.uw.edu/sites/default/files/sections/Registrar/Change-Student-Name.pdf",
            title: "Change Your Legal Name" } : null,
        (this.student || this.studEmployee) && this.isBothell ?
          { url: "https://www.uwb.edu/registration/policies/name-change",
            title: "Name Change Policy" } : null,
        (this.student || this.studEmployee) && !this.isTacoma && !this.isBothell ? 
          { url: "https://registrar.washington.edu/enrollment-and-records/name-change-policy/",
            title: "Change Your Legal Name" } : null,
        (this.student || this.studEmployee) && !this.isTacoma && !this.isBothell ? 
          { url: "https://depts.washington.edu/qcenter/wordpress/changing-your-name-in-the-uw-student-database/",
            title: "Changing Your Name and Gender" } : null,
        this.employee || this.studEmployee ?
          { url: "http://hr.uw.edu/benefits/life-events/change-your-address-name-gender-citizenship-or-birth-date/",
            title: "Change Your Personal Information" } : null,
        this.student ?
          { url: "https://registrar.washington.edu/enrollment-and-degree-verification/",
            title: "Self-Service Enrollment Verification" } : null,
      ].filter(x => x !== null);
    }
  },
};
</script>
