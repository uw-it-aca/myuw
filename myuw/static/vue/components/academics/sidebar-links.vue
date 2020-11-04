<template>
  <uw-panel
    :loaded="isReady" :mobile-only="mobileOnly"
  >
    <template #panel-body>
      <div v-for="linkCategory in linkData" :key="linkCategory.subcat_slug">
        <h3 :id="linkCategory.subcat_slug" class="h5">
          {{ linkCategory.subcategory }}
        </h3>
        <ul class="list-unstyled myuw-text-md mb-4">
          <li v-for="link in linkCategory.links" :key="link.url" class="mb-1">
            <a v-if="link.new_tab" :href="link.url" target="_blank">
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
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
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
    statusCode() {
      return this.statusCodeTagged(this.urlExtra);
    },
    showError: function() {
      return this.statusCode !== 404;
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
