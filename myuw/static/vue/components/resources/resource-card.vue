<template>
  <div>
    <b-card-group columns class="myuw-card-columns-2">
      <uw-card
        v-for="(resource, i) in Object.values(resource.subcategories)"
        :key="i"
        :id="resource.subcat_id"
        loaded
      >
        <template #card-heading>
          <div>
            <h4>
              {{resource.subcat_name}}
            </h4>
            <button v-if="!resource.is_pinned" @click="pin(resource)">
              Pin to Home
            </button>
            <button v-else @click="unpin(resource)">
              Unpin
            </button>
          </div>
        </template>
        <template #card-body>
          <ul>
            <li v-for="(link, i) in resource.links" :key="i">
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
  props: {
    resource: {
      type: Object,
      required: true,
    }
  },
  components: {
    'uw-card': Card,
  },
  methods: {
    ...mapActions('resources', ['pin', 'unpin']),
  }
}
</script>