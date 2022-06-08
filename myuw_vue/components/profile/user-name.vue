<template>
  <uw-panel v-if="hasName" :loaded="isReady" :errored="isErrored">
    <template #panel-body>
      <h2 class="h4 mb-3">
        <span v-if="hasPreferred">
          {{ titleCaseName(displayName) }}
          <span v-if="hasPronouns" class="myuw-text-md text-uppercase" title="Pronouns">
            ({{ titleCaseName(Pronouns) }})
          </span>
        </span>
      </h2>
    </template>
  </uw-panel>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Card,
  },
  data() {
    return {};
  },
  computed: {
    ...mapState({
      displayName: (state) => state.directory.value.display_name,
      fullName: (state) => state.directory.value.full_name,
      pronouns: (state) => state.directory.value.pronouns,
    }),
    ...mapGetters('directory', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    hasName() {
      return Boolean(this.displayName) || Boolean(this.fullName);
    },
    hasPreferred() {
      return Boolean(this.displayName) && this.displayName !== this.fullName;
    },
    hasPronouns() {
      return Boolean(this.pronouns && this.pronouns.length);
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
