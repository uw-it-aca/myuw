<template>
  <uw-card :loaded="isReady" :errored="isErrored" :errored-show="showError">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Name &amp; Pronouns</h2>
    </template>
    <template #card-body>
      <uw-card-property-group>
        <uw-card-property title="Official Name">
          {{ fullName }}
        </uw-card-property>

        <uw-card-property title="Preferred Name">
          <p v-if="!hasPreferredName" class="text-muted">No Preferred name listed</p>
          <div v-else>
            {{ prefName }}
          </div>
        </uw-card-property>
        <uw-card-property title="Pronouns">
          <div v-if="hasPronouns">
            {{ pronouns }}
          </div>
          <div v-else class="text-muted">No pronouns listed</div>
          <div class="mt-4">
            <uw-link-button
              class="px-2 py-1"
              href="https://identity.uw.edu/"
              >Edit in Identity.UW
            </uw-link-button>
          </div>
        </uw-card-property>
      </uw-card-property-group>
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import CardProperty from '../_templates/card-property.vue';
import CardPropertyGroup from '../_templates/card-property-group.vue';
import LinkButton from '../_templates/link-button.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-card-property': CardProperty,
    'uw-card-property-group': CardPropertyGroup,
    'uw-link-button': LinkButton,
  },
  computed: {
    ...mapState({
      fullName: (state) => state.directory.value.full_name,
      prefName: (state) => state.directory.value.display_name,
      pronouns: (state) => state.directory.value.pronouns,
    }),
    ...mapGetters('directory', {
      isReady: 'isReady',
      isErrored: 'isErrored',
    }),
    hasPreferredName() {
      return Boolean(this.prefName && this.prefName.length);
    },
    hasPronouns() {
      return Boolean(this.pronouns && this.pronouns.length);
    },
    showError() {
      return false;
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


