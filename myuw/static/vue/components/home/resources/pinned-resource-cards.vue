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
            {{resource.category_name}}
            <h3>
              {{subcategories.subcat_name}}
            </h3>
            <button @click="unpinWrapper(subcategories)">
              Unpin
            </button>
          </div>
        </template>
        <template #card-body>
          <ul>
            <li v-for="(link, k) in subcategories.links" :key="k">
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