<template>
  <div v-if="isReady">
    <div :class="[$mq === 'mobile' ? 'px-3' : 'px-0']">
      <h2 class="h4">On this page</h2>
      <div class="mt-3">
        <ul
          class="list-unstyled myuw-text-lg"
          :class="[$mq == 'desktop' ? 'myuw-column-count-2' : '']"
        >
          <li v-for="(resource, i) in resources" :key="i" class="mb-1">
            <a :href="`#${resource.category_id}`">{{ resource.category_name }}</a>
          </li>
        </ul>
      </div>
    </div>
    <div v-for="(resource, i) in resources" :key="i" class="mt-5">
      <h2 :id="resource.category_id" class="h4" :class="[$mq === 'mobile' ? 'px-3' : 'px-0']">
        {{ resource.category_name }}
      </h2>
      <uw-resource-card :resource="resource" />
    </div>
    <b-button
      variant="secondary"
      size="sm"
      class="position-sticky mb-3 mr-3 float-right text-center myuw-back-to-top"
      title="Back to Top"
      @click="scrollToTop"
    >
      <font-awesome-icon :icon="faChevronUp" size="lg" />
      <span class="d-block myuw-text-xs"><span class="sr-only">Back to</span> TOP</span>
    </b-button>
  </div>
</template>

<script>
import { faChevronUp } from '@fortawesome/free-solid-svg-icons';
import { mapGetters, mapState, mapActions } from 'vuex';
import ResourceCard from './resource-card.vue';

export default {
  components: {
    'uw-resource-card': ResourceCard,
  },
  data() {
    return {
      faChevronUp,
    };
  },
  computed: {
    ...mapState('resources', {
      resources: (state) => state.value[''],
    }),
    ...mapGetters('resources', ['isReady']),
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('resources', ['fetch']),
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
  },
};
</script>
<style lang="scss" scoped>
@import '../../../css/myuw/variables.scss';
.myuw-back-to-top {
  bottom: 1rem;
}
</style>