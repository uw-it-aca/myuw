<template>
  <uw-panel :loaded="isReady">
    <template #panel-body>
      <uw-sidelink-section
        v-for="linkCategory in linkData"
        :key="linkCategory.subcat_slug"
        :category-title="linkCategory.subcategory"
        :links="linkCategory.links"
      />
    </template>
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';
import SidelinkSection from '../_templates/sidelink-section.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-sidelink-section': SidelinkSection,
  },
  data: function() {
    return {
      urlExtra: 'pageacademics',
    };
  },
  computed: {
    ...mapState({
      linkData: function(state) {
        return state.category_links.value[this.urlExtra].link_data;
      },
    }),
    ...mapGetters('category_links', [
      'isReadyTagged',
      'isErroredTagged',
      'statusCodeTagged',
    ]),
    isReady() {
      return this.isReadyTagged(this.urlExtra);
    },
    isErrored() {
      return this.isErroredTagged(this.urlExtra);
    },
  },
  created() {
    this.fetch(this.urlExtra);
  },
  methods: {
    ...mapActions('category_links', ['fetch']),
  },
};
</script>
