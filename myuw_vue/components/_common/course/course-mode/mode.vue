<template>
  <div class="text-uppercase myuw-text-sm">
    <span v-if="section.is_asynchronous">
      Asynchronous Online (A)
      <a
        role="button"
        class="async-msg"
        data-bs-container="body"
        data-bs-toggle="popover"
        title="Asynchronous Online (A)"
        data-bs-placement="bottom"
        data-bs-html="true"
        data-bs-content="<p>Students and instructors always interact with others and engage course materials 
        asynchronously. While there are no regularly-scheduled, required synchronous class meetings, students 
        are expected to meet all assignment deadlines and may be asked to schedule occasional, brief synchronous 
        one-on-one check-in meetings with the instructors. <a href='https://registrar.washington.edu/classrooms/course-modes/'>
        Learn more about course modes.</a></p>
        <b>Incorrect course mode?</b>
        <div>In case of an error, contact your department time schedule coordinator.</div>"
    >
      <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
    </a>
    </span>
    <span v-else-if="section.is_synchronous">
      Synchronous Online (O)
      <a
        role="button"
        class="sync-msg"
        data-bs-container="body"
        data-bs-toggle="popover"
        title="Synchronous Online (O)"
        data-bs-placement="bottom"
        data-bs-html="true"
        data-bs-content="<p>Students and instructors interact online synchronously through regularly-scheduled, 
        required meetings using applications such as Zoom. Students should also expect to interact with 
        others and engage in course materials asynchronously. The time schedule contains information about 
        the course’s regular, required synchronous meeting time. <a href='https://registrar.washington.edu/classrooms/course-modes/'>
        Learn more about course modes.</a></p>
        <b>Incorrect course mode?</b>
        <div>In case of an error, contact your department time schedule coordinator.</div>"
    >
      <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
    </a>
    </span>
    <span v-else-if="section.is_hybrid">
      Hybrid (B)
      <a
        role="button"
        class="hybrid-msg"
        data-bs-container="body"
        data-bs-toggle="popover"
        title="Hybrid (B)"
        data-bs-placement="bottom"
        data-bs-html="true"
        data-bs-content="<p>Some, but not all, required class meetings occur in a physical classroom. When 
        not meeting in the physical classroom, students and instructors will attend class online, either 
        through required synchronous sessions or required asynchronous activities. The time schedule 
        contains information about the course’s required weekly physical classroom and synchronous 
        meeting time. <a href='https://registrar.washington.edu/classrooms/course-modes/'>Learn more about 
        course modes.</a></p>
        <b>Incorrect course mode?</b>
        <div>In case of an error, contact your department time schedule coordinator.</div>
"
    >
      <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
    </a>
    </span>
    <span v-else>
      In Person
      <a
        role="button"
        class="inperson-msg"
        data-bs-container="body"
        data-bs-toggle="popover"
        title="In Person"
        data-bs-placement="bottom"
        data-bs-html="true"
        data-bs-content="<p>All required class meetings occur in a physical classroom. The course may also have 
        online content and activities that students engage in outside of class time as homework or study 
        materials. The time schedule contains information about the course’s required weekly physical 
        classroom meeting time. <a href='https://registrar.washington.edu/classrooms/course-modes/'>Learn more about course modes.</a></p>
        <b>Incorrect course mode?</b>
        <div>In case of an error, contact your department time schedule coordinator.</div>"
    >
      <font-awesome-icon :icon="faQuestionCircle" class="text-dark-gray" />
    </a>
    </span>
    <a
      v-if="!hideInfoLink"
      v-out="'course-mode'"
      href="https://registrar.washington.edu/classrooms/course-modes/"
      :title="title"
    ><font-awesome-icon :icon="faQuestionCircle" /></a>
  </div>
</template>

<script>
import {
  faQuestionCircle,
} from '@fortawesome/free-solid-svg-icons';
import { Popover } from 'bootstrap';

export default {
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
  data() {
    return {
      faQuestionCircle,
    }
  },
  computed: {
    title() {
      return (
        this.includeTSC ?
        "Learn About Course Mode, in case of an error please" +
        "contact your department Time Schedule coordinator." :
        "Learn About Course Mode");
    },
  },
  mounted() {
    var popover = new Popover(document.querySelector('.async-msg'));
    var popover = new Popover(document.querySelector('.inperson-msg'));
    var popover = new Popover(document.querySelector('.sync-msg'));
    var popover = new Popover(document.querySelector('.hybrid-msg'));
  },
};
</script>
