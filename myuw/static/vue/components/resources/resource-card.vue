<template>
  <div>
    <b-card-group columns class="myuw-card-columns-2">
      <uw-card
        v-for="(subcatRes, i) in Object.values(resource.subcategories)"
        :id="subcatRes.subcat_id"
        :key="i"
        loaded
      >
        <template #card-heading>
          <div>
            <h4>
              {{subcatRes.subcat_name}}
            </h4>
            <button v-if="!subcatRes.is_pinned" @click="pin(subcatRes)">
              Pin to Home
            </button>
            <button v-else @click="unpin(subcatRes)">
              Unpin
            </button>
          </div>
        </template>
        <template #card-body>
          <ul>
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
  }
}
</script>