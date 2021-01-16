<template>
  <div>
    <b-card-group columns class="myuw-card-columns-2">
      <uw-card
        v-for="(resourceCat, i) in Object.values(resource.subcategories)"
        :id="resourceCat.subcat_id"
        :key="i"
        loaded
      >
        <template #card-heading>
          <div>
            <h4>
              {{resourceCat.subcat_name}}
            </h4>
            <button v-if="!resourceCat.is_pinned" @click="pin(resourceCat)">
              Pin to Home
            </button>
            <button v-else @click="unpin(resourceCat)">
              Unpin
            </button>
          </div>
        </template>
        <template #card-body>
          <ul>
            <li v-for="(link, j) in resourceCat.links" :key="j">
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
  }
}
</script>