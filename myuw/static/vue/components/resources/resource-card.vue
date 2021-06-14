<template>
  <div>
    <b-card-group columns class="mt-3" :class="[$mq != 'mobile' ? 'myuw-column-count-2' : '']">
      <uw-card
        v-for="(subcatRes, i) in Object.values(resource.subcategories)"
        :id="subcatRes.subcat_id"
        :key="i"
        loaded
        :class="[$mq === 'mobile' ? '' : 'resource-card']"
      >
        <template #card-heading>
          <div>
            <h3 class="h6 text-dark-beige myuw-font-encode-sans d-inline-block">
              {{subcatRes.subcat_name}}
            </h3>
            <b-button
              v-if="!subcatRes.is_pinned"
              variant="link"
              class="myuw-text-sm text-muted"
              :title="`Add ${subcatRes.subcat_name} resources to home page`"
              @click="pinWrapper(subcatRes)"
            >
              Pin to Home
            </b-button>
            <b-button
              v-else
              variant="link"
              class="myuw-text-sm text-muted"
              :title="`Remove ${subcatRes.subcat_name} resources from home page`"
              @click="unpinWrapper(subcatRes)"
            >
              Unpin
            </b-button>
          </div>
        </template>
        <template #card-body>
          <ul class="list-unstyled myuw-text-md mb-0">
            <li v-for="(link, j) in subcatRes.links" :key="j" class="mb-1">
              <a :href="link.url">{{link.title}}</a>
            </li>
          </ul>
        </template>
      </uw-card>
    </b-card-group>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Card from '../_templates/card.vue';

export default {
  components: {
    'uw-card': Card,
  },
  props: {
    resource: {
      type: Object,
      required: true,
    }
  },
  methods: {
    ...mapActions('resources', ['pin', 'unpin']),
    pinWrapper(subcatRes) {
      this.$logger.cardPin(this, subcatRes.subcat_id);
      this.pin(subcatRes);
    },
    unpinWrapper(subcatRes) {
      this.$logger.cardUnPin(this, subcatRes.subcat_id);
      this.unpin(subcatRes);
    },
  }
}
</script>
<style lang="scss" scoped>
.resource-card {
  margin-bottom: 6px !important;
  &:not(:hover) {
    background-color: rgba(0,0,0,0);
    border: solid 1px transparent;
    box-shadow: none !important;
  }
}
</style>
