<template>
  <div>
    <h4 class="myuw-card-heading">
      Visa and Immigration Rules
    </h4>

    <ul class="unstyled-list">
      <li>
        <a
          href="http://www.uwb.edu/cie/current-students/travel"
          target="_blank"
          aria-label="Travel and Visas for Int'l Students"
        >Travel and Visas</a>
      </li>
      <li>
        <a
          href="https://www.uwb.edu/cie/current-students/immigration-documents"
          target="_blank"
          aria-label="Immigration Rules for F-1 students"
        >Immigration Document for F-1 Students</a>
      </li>
      <li>
        <a
          href="https://www.uwb.edu/cie/current-students/vacation-quarter"
          target="_blank"
          aria-label="Vacation Quarter"
        >Vacation Quarter</a>
      </li>
      <li>
        <a
          href="http://www.uwb.edu/cie/employment"
          target="_blank"
          aria-label="Int'l Student Employment"
        >Employment and Internships</a>
      </li>
      <li>
        <a
          href="https://www.uwb.edu/cie/events"
          target="_blank"
          aria-label="Center for International Education Event Calendar"
        >Center for International Education (CIE) Calendar</a>
      </li>
    </ul>

    <h4 class="myuw-card-heading">
      Academic Support
    </h4>
    <ul class="unstyled-list">
      <li>
        <a
          href="http://www.uwb.edu/cie/current-students/writing-support"
          target="_blank"
          aria-label="Writing Support and Resources"
        >Writing Support and Resources</a>
      </li>
      <li>
        <a
          href="http://www.uwb.edu/wacc"
          target="_blank"
          aria-label="Writing and Communication Center (WaCC)"
        >Writing and Communication Center (WaCC)</a>
      </li>
      <li>
        <a
          href="https://www.uwb.edu/qsc"
          target="_blank"
          aria-label="Quantitative Skills Center (QSC)"
        >Quantitative Skills Center (QSC)</a>
      </li>
    </ul>
  </div>
</template>

<script>
import {mapState} from 'vuex';

export default {
  data: function() {
    return {};
  },
  computed: mapState({
    user: (state) => state.user,
  }),
};
</script>
