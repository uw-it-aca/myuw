<template>
  <uw-card v-if="true" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation: Pre Application</h2>
    </template>
    <template #card-body>
      <p>
        <strong>To graduate, you'll need apply.</strong> Dont worry, it's an easy process you 
        complete with your departmental adviser!
      </p>
    </template>
    <template #card-disclosure>
      <b-collapse :id="`collapseGraduationContent`" v-model="isOpen">
        <ul class="list-style">
          <li> <strong>Deadline:</strong> The third Friday of the quarter in which you intend to graduate.</li>
          <li> <strong>Submit early:</strong> If you apply 2-3 quarters before graduation, you get Graduating Senior Priority 
          for registration for 2 quarters.</li>
        </ul>
        <p>
        <strong>Get all the details:</strong> Follow the <a href="https://www.washington.edu/students/graduation-checklist/">UW Graduation checklist</a>.
        </p>
        <p>
          International students, review the <a href="https://iss.washington.edu/resources/final-checklist/">ISS Graduation checklist</a> 
          for additional guidance.
        </p>
      </b-collapse>
    </template>
    <template #card-footer>
      <button
        v-b-toggle="`collapseGraduationContent`"
        type="button"
        class="btn btn-link w-100 p-0 border-0 text-dark"
      >
        Deadlines and details
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';

import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data() {
    return {
      isOpen: false,
      faChevronUp,
      faChevronDown,
    };
  },
  watch: {},
  computed: {},

  mounted() {
    this.getOpen();
  },

  methods: {
    getOpen: function () {
      let blah = document.querySelector('#collapseGraduationContent');
      if (blah.classList.contains('show')) {
        console.log('shown');
      } else {
        console.log('hidden');
      }
    },
  },
};
</script>

<style lang="scss" scoped></style>
