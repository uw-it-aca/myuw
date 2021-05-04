<template>
  <uw-card
    :loaded=true
  >
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Your Advisers
      </h2>
    </template>
    <template #card-body>
      <div>
        <strong>Major</strong>
        Premajor
      </div>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Card from '../_templates/card.vue';
export default {
  components: {
    'uw-card': Card,
  },
};
</script>


