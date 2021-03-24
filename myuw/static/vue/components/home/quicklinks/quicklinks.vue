<template>
  <uw-card :loaded="isReady" :errored="isErrored" :mobile-only="mobileOnly">
    <template #card-heading>
      <h2 class="h4 mb-3 text-dark-beige myuw-font-encode-sans">
        Quick Links
      </h2>
    </template>
    <template #card-body>
      <ul class="list-unstyled myuw-text-md">
        <uw-link
          v-for="(link, index) in defaultLinks"
          :key="`default-${index}`"
          :link="link" :buttons="['remove']"
          :custom-id="`default-${index}`"
        />
        <uw-link
          v-for="(link, index) in customLinks" :key="`custom-${index}`"
          :link="link" :buttons="['edit', 'remove']"
          :custom-id="`custom-${index}`" can-actually-remove
        />
      </ul>

      <uw-covid-links :links="allLinks" />

      <div v-if="recentLinks.length">
        <h3 class="h6">
          Recently Visited
        </h3>
        <ul class="list-unstyled myuw-text-md">
          <uw-link
            v-for="(link, index) in recentLinks" :key="`recent-${index}`"
            :link="link" :buttons="['save']" :custom-id="`recent-${index}`"
          />
        </ul>
        <p class="m-0 myuw-text-md">
          Save your recently visited links for future access.
        </p>
      </div>
      <hr v-if="recentLinks.length">
      <p class="m-0 myuw-text-md">
        <span>
          Not seeing the links you're looking for?
          <span v-if="popularLinks.length">
            Select from
            <b-button v-b-toggle.popular_qlinks variant="link" size="sm"
                      :disabled="disableActions"
                      class="d-inline-block align-bottom p-0 border-0"
            >
              popular links
            </b-button>, or
          </span>
          <b-button v-b-toggle.custom_qlinks variant="link" size="sm"
                    :disabled="disableActions"
                    class="d-inline-block align-bottom p-0 border-0"
          >
            <span v-if="popularLinks.length">add your own</span>
            <span v-else>Add your own</span>
          </b-button>.
        </span>
      </p>

      <b-collapse id="popular_qlinks" class="bg-light mx-n3 p-3 mt-3">
        <h3 class="h6">
          Popular Links
        </h3>
        <ul class="list-unstyled myuw-text-md mb-0">
          <uw-link
            v-for="(link, index) in popularLinks" :key="`popular-${index}`"
            :link="link" :buttons="['save']" :custom-id="`popular-${index}`"
          />
        </ul>
      </b-collapse>

      <b-collapse
        id="custom_qlinks"
        role="form"
        class="bg-light mx-n3 p-3 mt-3"
      >
        <b-form class="myuw-text-md" @submit="addLink" @reset="onReset">
          <h3 class="h6">
            Add your link to Quick Links
          </h3>
          <b-form-group label="URL" label-for="myuw-custom-qlink">
            <b-form-input
              id="myuw-custom-qlink"
              v-model="customLink.url"
              type="url"
              placeholder="https://www.washington.edu"
              required
              size="sm"
            />
          </b-form-group>
          <b-form-group
            label="Link name (optional)"
            label-for="myuw-custom-qlink-label"
          >
            <b-form-input
              id="myuw-custom-qlink-label"
              v-model="customLink.label"
              type="text"
              placeholder="UW Homepage"
              size="sm"
            />
          </b-form-group>
          <div>
            <div v-if="isAddErrored" id="error_saving">
              <span class="text-danger">Error saving</span>
            </div>
            <div v-if="isAddFetching" id="quicklink_saving">
              <span class="text-muted">Saving...</span>
            </div>
          </div>
          <div class="d-flex justify-content-end">
            <b-button v-b-toggle.custom_qlinks
                      variant="link" type="reset" size="sm"
            >
              Cancel
            </b-button>
            <b-button  v-b-toggle.custom_qlinks
                       variant="primary" type="submit" size="sm"
            >
              Add
            </b-button>
          </div>
        </b-form>
      </b-collapse>
    </template>
  </uw-card>
</template>

<script>
import {mapGetters, mapState, mapActions} from 'vuex';

import Card from '../../_templates/card.vue';
import Link from './link.vue';
import CovidLinks from './covid-links.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link': Link,
    'uw-covid-links': CovidLinks,
  },
  props: {
    mobileOnly: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      customLink: {},
    };
  },
  computed: {
    ...mapState({
      disableActions: (state) => state.disableActions,
    }),
    ...mapState('quicklinks', {
      recentLinks: (state) => state.value.recent_links,
      popularLinks: (state) => state.value.popular_links,
      customLinks: (state) => state.value.custom_links,
      defaultLinks: (state) => state.value.default_links,
      allLinks: (state) => state.value,
    }),
    ...mapGetters('quicklinks', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      isAddFetching: 'isAddFetching',
      isAddErrored: 'isAddErrored',
    }),
  },
  created() {
    this.fetch();
  },
  methods: {
    ...mapActions('quicklinks', {
      fetch: 'fetch',
      quicklinksAddLink: 'addLink',
    }),
    addLink: function(event) {
      event.preventDefault();
      this.$logger.quicklink('add', this.customLink.url);
      this.quicklinksAddLink(this.customLink);
    },
    onReset: function(event) {
      event.preventDefault();
      this.customLink = {};
    },
  },
};
</script>

