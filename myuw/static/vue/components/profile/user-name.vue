<template>
  <uw-panel
      v-if="hasName"
      :loaded="isReady"
      :errored="isErrored"
  >
    <template #panel-body>
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
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Card,
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
