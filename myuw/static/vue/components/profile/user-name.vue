<template>
  <uw-card
      v-if="showCard"
      :loaded="isReady"
      :errored="isErrored"
      :errored-show="false"
  >
    <template #card-heading>
      <h2 class="heading-profile">
        <span v-if="hasPreferred">{{ titleCaseName(displayName) }}
          ({{ titleCaseName(fullName) }})</span>
        <span v-else>{{ titleCaseName(fullName) }}</span>
        &nbsp;
        <a
          href="https://identity.uw.edu/"
          title="Manage your preferred name"
          data-linklabel="Manage preferred name - Identity.UW">
            <i class="fa fa-pencil" aria-hidden="true"></i>
            <span class="sr-only">Manage your preferred name</span>
        </a>
      </h2>
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
      displayName: (state) => state.directory.value.display_name,
      fullName: (state) => state.directory.value.full_name,
    }),
    ...mapGetters('directory', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    hasName() {
      return this.displayName !== undefined || this.fullName !== undefined;
    },
    showCard() {
      return !this.isReady || this.hasName;
    },
    hasPreferred() {
      return this.displayName !== undefined &&
        this.displayName !== this.fullName;
    },
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('directory', {
      fetch: 'fetch',
    }),
  },
};
</script>
