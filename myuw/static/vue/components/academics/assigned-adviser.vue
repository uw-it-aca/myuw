<template>
  <uw-card
    :loaded="isReady"
    :errored="isErrored"
    :errored-show="showError"
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Advisers
      </h2>
    </template>
    <template #card-body>
      <div>
        <strong>Major</strong>
        Premajor
      </div>
    </template>
    <template #card-error>
      An error occurred and MyUW cannot load your adviser information
      right now. In the meantime, try the
      <a v-out="'Advisers'"
        href=""
      >[ADVISER LINK PLACEHOLDER]</a>.
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
export default {
  components: {
    'uw-card': Card,
  },
  computed: {
    ...mapState({
      advisers: (state) => state.advisers.value,
    }),
    ...mapGetters('advisers', [
      'isReady',
      'isErrored',
      'statusCode',
    ]),
    showError: function() {
      return this.statusCode !== 404;
    },
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('advisers', ['fetch']),
  },
};
</script>


