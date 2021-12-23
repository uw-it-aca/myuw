<template>
  <uw-card v-if="true" :loaded="true">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Graduation: Pre Application</h2>
    </template>
    <template #card-body>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis dolorem labore a sit
        placeat nisi iusto ullam, ipsam vitae numquam ad, magni at ex quas ut magnam dignissimos
        incidunt nostrum.
      </p>
    </template>
    <template #card-disclosure>
      <b-collapse :id="`collapseGraduationContent`" v-model="isOpen">
        <p>this is the disclosure content</p>
        <p>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Debitis dolorem labore a sit
          placeat nisi iusto ullam, ipsam vitae numquam ad, magni at ex quas ut magnam dignissimos
          incidunt nostrum.
        </p>
      </b-collapse>
    </template>
    <template #card-footer>
      <button
        v-b-toggle="`collapseGraduationContent`"
        type="button"
        class="btn btn-link w-100 p-0 border-0 text-dark"
      >
        show more content
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
