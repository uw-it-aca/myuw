<template>
  <div v-if="isReady">
    <div v-for="(resource, i) in pinnedResources" :key="i">
      <uw-card
        v-for="(subcategories, j) in Object.values(resource.subcategories)"
        :key="j"
        :id="subcategories.subcat_id"
        loaded
      >
        <template #card-heading>
          <div>
            {{resource.category_name}}
            <h4>
              {{subcategories.subcat_name}}
            </h4>
            <button v-if="!subcategories.is_pinned" @click="pin(subcategories)">
              Pin to Home
            </button>
            <button v-else @click="unpin(subcategories)">
              Unpin
            </button>
          </div>
        </template>
        <template #card-body>
          <ul>
            <li v-for="(link, i) in subcategories.links" :key="i">
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
import Card from '../_templates/card.vue';

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
    pinnedResources() {
      return this.resources[this.urlExtra];
    },
    isReady() { return this.isReadyTagged(this.urlExtra); }
  },
  mounted() {
    this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('resources', ['fetch', 'pin', 'unpin']),
  }
}
</script>