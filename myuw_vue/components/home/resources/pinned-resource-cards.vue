<template>
  <div v-if="isReady">
    <div v-for="(resource, i) in maybePinnedResources" :key="i">
      <uw-card
        v-for="(subcategories, j) in pinnedSubcategories(resource.subcategories)"
        :id="subcategories.subcat_id"
        :key="j"
        loaded
      >
        <template #card-heading>
          <div>
            <button type="button"
              class="btn btn-link myuw-text-sm text-muted float-end"
              :title="`Remove ${subcategories.subcat_name} resources from home page`"
              @click="unpinWrapper(subcategories)"
            >
              Unpin
            </button>
            UW Resources
            <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
              {{subcategories.subcat_name}}
            </h2>
            
          </div>
        </template>
        <template #card-body>
          <ul class="list-unstyled myuw-text-md">
            <li v-for="(link, k) in subcategories.links" :key="k" class="mb-1">
              <a :href="link.url">{{link.title}}</a>
            </li>
          </ul>
        </template>
      </uw-card>
    </div>
  </div>
  <uw-card v-else />
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  data() {
    return {
      urlExtra: 'pinned/',
    };
  },
  computed: {
    ...mapState('resources', {
      resources: (state) => state.value, 
    }),
    ...mapGetters('resources', ['isReadyTagged']),
    // Maybe pinned because the pin/unpin only updates
    // the flag and does not remove the resource
    maybePinnedResources() {
      return this.resources[this.urlExtra];
    },
    isReady() { return this.isReadyTagged(this.urlExtra); }
  },
  mounted() {
    this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('resources', ['fetch', 'unpin']),
    pinnedSubcategories(subcategories) {
      return Object.values(subcategories).filter((s) => s.is_pinned);
    },
    unpinWrapper(subcategories) {
      this.$logger.cardUnPin(this, subcategories.subcat_id);
      this.unpin(subcategories);
    }
  }
}
</script>