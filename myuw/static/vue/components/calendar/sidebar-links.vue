<template>
  <div v-if="isReady">
    <uw-panel v-for="(linkData, i) in pagecalendarLinks.link_data" :key="i" loaded>
      <template #panel-body>
        <h2 class="h5">{{linkData.subcategory}}</h2>
        <ul class="list-unstyled myuw-text-md mb-4">
          <li v-for="(link, j) in linkData.links" :key="j" class="mb-1">
            <a :href="link.url">{{link.title}}</a>
          </li>
        </ul>
      </template>
    </uw-panel>
  </div>
</template>

<script>
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import {mapGetters, mapState, mapActions} from 'vuex';
import Panel from '../_templates/panel.vue';

export default {
  components: {
    'uw-panel': Panel,
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