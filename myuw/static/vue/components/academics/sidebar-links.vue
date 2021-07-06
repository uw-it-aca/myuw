<template>
  <uw-panel :loaded="isReady">
    <template #panel-body>
      <div v-for="linkCategory in linkData" :key="linkCategory.subcat_slug">
        <h2 :id="linkCategory.subcat_slug" class="h5">
          {{ linkCategory.subcategory }}
        </h2>
        <ul class="list-unstyled myuw-text-md">
          <li v-for="link in linkCategory.links" :key="link.url" class="mb-1">
            <a v-if="link.new_tab" :href="link.url">
              {{ link.title }}
            </a>
            <a v-else :href="link.url">
              {{ link.title }}
            </a>
          </li>
        </ul>
      </div>
    </template>
  </uw-panel>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
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
