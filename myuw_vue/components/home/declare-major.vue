<template>
  <uw-card v-if="showCard" :loaded="showContent" :errored="isErrored" :errored-show="false">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">Deciding on a Major</h2>
    </template>

    <template #card-body>
      Lorem ipsum dolor sit amet, consectetur adipisicing elit. Iusto est libero quas quidem
      exercitationem itaque natus beatae vero ut numquam, neque repudiandae eum modi dolorum animi
      fuga facere aut dolores!
    </template>

    <template #card-disclosure>
      <uw-collapse id="collapseDeclareMajor" v-model="isOpen">
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Non ullam, vitae laboriosam
        corrupti cumque reiciendis obcaecati praesentium neque sequi numquam maiores, corporis modi
        eligendi. Facilis amet omnis rem eveniet quia?
      </uw-collapse>
    </template>

    <template #card-footer>
      <button
        v-uw-collapse.collapseDeclareMajor
        type="button"
        class="btn btn-link btn-sm w-100 p-0 text-dark"
      >
        Learn more about how to get started
        <font-awesome-icon v-if="!isOpen" :icon="faChevronDown" class="align-middle" />
        <font-awesome-icon v-else :icon="faChevronUp" class="align-middle" />
      </button>
    </template>
  </uw-card>
</template>

<script>
// MUWM-5144 Pre-application
import { faChevronUp, faChevronDown } from '@fortawesome/free-solid-svg-icons';
// import { mapGetters, mapState, mapActions } from 'vuex';
import Card from '../_templates/card.vue';
import Collapse from '../_templates/collapse.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-collapse': Collapse,
  },
  data() {
    return {
      isOpen: false,
      showCard: true,
      showContent: true,
      faChevronUp,
      faChevronDown,
    };
  },
  computed: {},
  created() {},
  methods: {},
};
</script>

<style lang="scss" scoped></style>
