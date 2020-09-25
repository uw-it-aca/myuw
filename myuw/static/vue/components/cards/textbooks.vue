<template>
  <uw-card>
    <template #card-heading>
    </template>
    <template #card-body>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../../containers/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data: function() {
    return {
      term: 'current',
    };
  },
  computed: {
    ...mapGetters('textbooks', [
      'isReadyTagged',
      'isErroredTagged',
    ]),
  },
  // Called when the function in injected into the page
  created() {
    let urlSuffix = `${this.year},${this.term}`;

    if (this.summerTerm) {
      urlSuffix += `,${this.summerTerm}`;
    }
    // We got this fetch function from mapActions
    this.fetch(urlSuffix);
  },
  methods: {
    // Mapping the fetch function from textbooks module
    ...mapActions('textbooks', ['fetch']),
  },
};
</script>

<style lang="scss" scoped>
</style>
