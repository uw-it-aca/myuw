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

    linkList() {
      return [
        this.isBothell ?
          { url: "https://www.uwb.edu/facility/mail-services", title: "Mailing Services" } : null,
        this.student && this.isTacoma ?
          { url: "https://www.tacoma.uw.edu/registrar/changes-personal-data#permalink-4977",
            title: "Preferred Names" } : null,
        (this.student || this.studEmployee) && !this.isTacoma && !this.isBothell ? 
          { url: "https://registrar.washington.edu/students/personal-data/names/",
            title: "Student Name and Updates" } : null,
        this.student && !this.isTacoma && !this.isBothell ? 
          { url: "https://registrar.washington.edu/students/personal-data/preferred-names-faqs/",
            title: "Preferred Names FAQ" } : null,
        (this.student || this.studEmployee) && this.isTacoma ?
          { url: "https://www.tacoma.uw.edu/registrar/changes-personal-data#permalink-10969",
            title: "Change Your Legal Name" } : null,
        (this.student || this.studEmployee) && this.isBothell ?
          { url: "https://www.uwb.edu/registration/policies/name-change",
            title: "Name Change Policy" } : null,
        (this.student || this.studEmployee) && !this.isTacoma && !this.isBothell ? 
          { url: "https://registrar.washington.edu/students/personal-data/gender-identity/",
            title: "Gender Identity & Updates" } : null,
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
