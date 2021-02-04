<template>
  <div v-if="isReady">
    <h3>
      On this page
    </h3>
    <ul>
      <li v-for="(resource, i) in resources" :key="i">
        <a :href="`#${resource.category_id}`">{{resource.category_name}}</a>
      </li>
    </ul>
    <div v-for="(resource, i) in resources" :key="i">
      <h3 :id="resource.category_id">
        {{resource.category_name}}
      </h3>
      <uw-resource-card :resource="resource"/>
    </div>
    <button type="button" id='scroll-to-top' class="myuw-back-to-top" title="Back to Top" data-spy="affix" data-offset-bottom="110">
        <font-awesome-icon :icon="['fa', 'chevron-up']" />
        <span><span class="sr-only">Back to</span> Top</span>
    </button>
  </div>
</template>

<script>
import { mapGetters, mapState, mapActions } from 'vuex';
import ResourceCard from './resource-card.vue';

export default {
  components: {
    'uw-resource-card': ResourceCard,
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
  }
}
</script>