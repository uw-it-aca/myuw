<template>
  <div class="text-uppercase myuw-text-sm">
    <span v-if="section.is_asynchronous">
      Asynchronous Online (A)
      <uw-pop-over v-if="!hideInfoLink"
        :selector="`async-msg-${section.id}`" title="Asynchronous Online (A)"
        :content="asyncMsg"/>
    </span>
    <span v-else-if="section.is_synchronous">
      Synchronous Online (O)
      <uw-pop-over v-if="!hideInfoLink"
        :selector="`sync-msg-${section.id}`" title="Synchronous Online (O)"
        :content="syncMsg"/>
    </span>
    <span v-else-if="section.is_hybrid">
      Hybrid (B)
      <uw-pop-over v-if="!hideInfoLink"
        :selector="`hybrid-msg-${section.id}`" title="Hybrid (B)" :content="hybMsg"/>
    </span>
    <span v-else>
      In Person
      <uw-pop-over v-if="!hideInfoLink"
        :selector="`inperson-msg-${section.id}`" title="In Person" :content="inPersonMsg"/>
    </span>
  </div>
</template>

<script>
import PopOver from '../../pop-over.vue';

export default {
  components: {
    'uw-pop-over': PopOver,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    hideInfoLink: {
      type: Boolean,
      default: false,
    },
    includeTSC: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    learnMoreMsg() {
      return " <a href='https://registrar.washington.edu/classrooms/course-modes/'>" +
        "Learn more about course modes.</a></p>";
    },
    contactTsMsg() {
      return "<b>Incorrect course mode?</b>" +
        "<div>In case of an error, contact your department time schedule coordinator.</div>";
    },
    asyncMsg() {
      const msg = (
        "<p>Students and instructors always interact with others and engage course materials" +
        " asynchronously. While there are no regularly-scheduled, required synchronous class" +
        " meetings, students are expected to meet all assignment deadlines and may be asked " +
        "to schedule occasional, brief synchronous one-on-one check-in meetings with the " +
        "instructors.");
      return (this.includeTSC
        ? (msg + this.learnMoreMsg + this.contactTsMsg) : msg);
    },
    syncMsg() {
      const msg = (
        "Students and instructors interact online synchronously through regularly-scheduled, " +
        "required meetings using online applications. Students should also expect to " +
        "interact with others and engage in course materials asynchronously. The time schedule" +
        " contains information about the course’s regular, required synchronous meeting time.");
      return (this.includeTSC
        ? (msg + this.learnMoreMsg + this.contactTsMsg) : msg);
    },
    hybMsg() {
      const msg = (
        "Some, but not all, required class meetings occur in a physical classroom. When not " +
        "meeting in the physical classroom, students and instructors will attend class online," +
        " either through required synchronous sessions or required asynchronous activities. " +
        "The time schedule contains information about the course’s required weekly physical " +
        "classroom and synchronous meeting time (e.g., MW 1-2pm in-person, F 1-2pm online).");
      return (this.includeTSC
        ? (msg + this.learnMoreMsg + this.contactTsMsg) : msg);
    },
    inPersonMsg() {
      const msg = (
        "All required class meetings occur in a physical classroom. The course may also have " +
        "online content and activities that students engage in outside of class time as homework" +
        " or study materials. The time schedule contains information about the course’s required" +
        " weekly physical classroom meeting time.");
      return (this.includeTSC
        ? (msg + this.learnMoreMsg + this.contactTsMsg) : msg);
    },
  },
};
</script>
