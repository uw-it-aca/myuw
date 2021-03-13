<template>
  <uw-panel
      v-if="hasName"
      :loaded="isReady"
      :errored="isErrored"
  >
    <template #panel-body>
      <h3>
        <span v-if="hasPreferred">{{ titleCaseName(displayName) }}
          <span class="myuw-text-md text-uppercase">({{ titleCaseName(fullName) }})</span>
        </span>
        <span v-else>{{ titleCaseName(fullName) }}</span>
        <a
          v-out="'Manage preferred name - Identity.UW'"
          href="https://identity.uw.edu/"
          title="Manage your preferred name">
            <font-awesome-icon :icon="['fas', 'pencil-alt']" class="myuw-text-md" />
            <span class="sr-only">Manage your preferred name</span>
        </a>
      </h3>
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
