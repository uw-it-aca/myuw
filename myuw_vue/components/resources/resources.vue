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
    <div v-for="(resource, i) in resources" :key="i">
      <hr class="bg-secondary">
      <h2 :id="resource.category_id" class="h4"
        :class="[$mq === 'mobile' ? 'px-3' : 'px-0']">
        {{ resource.category_name }}
      </h2>
      <uw-resource-card :resource="resource" />
    </div>
    <button type="button"
      class="btn btn-secondary position-sticky mb-3 me-3 float-end text-center myuw-back-to-top"
      title="Back to Top"
      @click="scrollToTop"
    >
      <font-awesome-icon :icon="faChevronUp" size="lg" />
      <span class="d-block myuw-text-xs"><span class="visually-hidden">Back to</span> TOP</span>
    </button>
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
  watch: {
    isReady: function () {
      this.scrollToFragment();
    }
  },
  mounted() {
    this.fetch();
  },
  methods: {
    ...mapActions('resources', ['fetch']),
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    scrollToFragment() {
      this.$nextTick(() => {
        if (window.location.hash) {
          document.getElementById(window.location.hash.substring(1)).scrollIntoView({ behavior: 'smooth' });
        }
      });
    },
  },
};
</script>
<style lang="scss" scoped>
@import '../../../myuw/static/css/myuw/variables.scss';
.myuw-back-to-top {
  bottom: 1rem;
}
</style>