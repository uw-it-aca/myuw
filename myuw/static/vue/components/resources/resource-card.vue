<template>
  <div>
    <b-card-group columns :class="[$mq == 'desktop' ? 'myuw-column-count-2' : '']">
      <uw-card
        v-for="(subcatRes, i) in Object.values(resource.subcategories)"
        :id="subcatRes.subcat_id"
        :key="i"
        loaded
      >
        <template #card-heading>
          <div>
            <h3 class="h6 d-inline-block">
              {{subcatRes.subcat_name}}
            </h3>
            <b-button variant="link" class="myuw-text-sm text-muted" v-if="!subcatRes.is_pinned" @click="pinWrapper(subcatRes)">
              Pin to Home
            </b-button>
            <b-button variant="link" class="myuw-text-sm text-muted" v-else @click="unpinWrapper(subcatRes)">
              Unpin
            </b-button>
          </div>
        </template>
        <template #card-body>
          <ul class="list-unstyled myuw-text-md">
            <li v-for="(link, j) in subcatRes.links" :key="j">
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