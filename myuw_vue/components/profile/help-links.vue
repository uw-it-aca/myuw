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
      isTacomaStud: (state) => state.user.affiliations.tacoma,
      isBothellStud: (state) => state.user.affiliations.bothell,
    }),
    nonBotTacStudent() {
      return (this.student || this.studEmployee) && !this.isTacomaStud && !this.isBothellStud;
    },
    linkList() {
      return [
        this.isBothellStud ?
          { url: "https://www.uwb.edu/facility/mail-services",
            title: "Mailing Services" } : null,
        this.isTacomaStud ?
          { url: "https://www.tacoma.uw.edu/registrar/changes-personal-data#permalink-10969",
            title: "Change Your Legal Name" } : null,
        this.isBothellStud ?
          { url: "https://www.uwb.edu/registration/policies/name-change",
            title: "Name Change Policy" } : null,
        this.nonBotTacStudent ?
          { url: "https://registrar.washington.edu/students/personal-data/names/",
            title: "Student Name and Updates" } : null,
        this.isTacomaStud ?
          { url: "https://www.tacoma.uw.edu/registrar/changes-personal-data#permalink-4977",
            title: "Preferred Names" } : null,
        this.nonBotTacStudent ?
          { url: "https://registrar.washington.edu/students/personal-data/preferred-names-faqs/",
            title: "Preferred Names FAQ" } : null,
        this.nonBotTacStudent ?
          { url: "https://registrar.washington.edu/students/personal-data/gender-identity/",
            title: "Gender Identity & Updates" } : null,
        this.employee || this.studEmployee ?
          { url: "https://isc.uw.edu/using-workday/managing-your-personal-and-work-information/",
            title: "Change Your Personal Information" } : null,
        this.student ?
          { url: "https://registrar.washington.edu/students/enrollment-and-degree-verification/",
            title: "Self-Service Enrollment Verification" } : null,
      ].filter(x => x !== null);
    }
  },
};
</script>
