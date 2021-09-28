<template>
  <uw-panel :loaded="isReady">
    <template #panel-body>
      <uw-sidelink-section
        v-for="linkCategory in pagecalendarLinks.link_data"
        :key="linkCategory.subcat_slug"
        :category-title="linkCategory.subcategory"
        :links="linkCategory.links"
      />
    </template>
  </uw-panel>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';
import SidelinkSection from '../_templates/sidelink-section.vue';

export default {
  components: {
    'uw-panel': Panel,
    'uw-sidelink-section': SidelinkSection,
  },
  data() {
    return {
      faCircle,
      urlExtra: 'pagecalendar',
    };
  },
  computed: {
    ...mapState('category_links', {
      allLinks: (state) => state.value,
    }),
    ...mapGetters('category_links', {
      isReadyTagged: 'isReadyTagged',
      isErroredTagged: 'isErroredTagged',
    }),
    pagecalendarLinks() {
      return this.allLinks[this.urlExtra];
    },
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
}
</script>