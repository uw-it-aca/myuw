<template>
  <div v-if="isReady">
    <h2 class="h4">
      On this page
    </h2>
    <b-container fluid class="mt-3">
      <ul class="list-unstyled myuw-text-lg row row-cols-1 row-cols-md-2">
        <li class="col" v-for="(resource, i) in resources" :key="i">
          <a :href="`#${resource.category_id}`">{{resource.category_name}}</a>
          <hr>
        </li>
      </ul>
    </b-container>
    <div v-for="(resource, i) in resources" :key="i">
      <h2 class="h4" :id="resource.category_id">
        {{resource.category_name}}
      </h2>
      <uw-resource-card :resource="resource"/>
    </div>
    <button type="button" class="myuw-back-to-top"
      title="Back to Top" @click="scrollToTop">
        <font-awesome-icon :icon="['fa', 'chevron-up']" />
        <span><span class="sr-only">Back to</span> Top</span>
    </button>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import ResourceCard from './resource-card.vue';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-resource-card': ResourceCard,
    'uw-panel': Panel,
  },
  computed: {
    ...mapState('resources', {
      resources: (state) => state.value[''], 
    }),
    ...mapGetters('resources', ['isReady'])
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('resources', ['fetch']),
    scrollToTop() {
      window.scrollTo({top: 0, behavior: 'smooth'});
    },
  }
}
</script>