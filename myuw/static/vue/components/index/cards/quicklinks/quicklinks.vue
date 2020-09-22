<template>
  <uw-card :loaded="true" :errored="false" :mobile-only="mobileOnly">
    <template #card-heading>
      <h3 class="text-dark-beige">
        Quick Links
      </h3>
    </template>
    <template #card-body>
      <ul class="list-unstyled myuw-text-md">
        <uw-link
          v-for="(link, index) in defaultLinks" :key="`default-${index}`"
          :link="link" :buttons="['remove']" :custom-id="`default-${index}`"
        />
        <uw-link
          v-for="(link, index) in customLinks" :key="`custom-${index}`"
          :link="link" :buttons="['edit', 'remove']"
          :custom-id="`custom-${index}`" can-actually-remove
        />
      </ul>
      <hr>
      <div v-if="recentLinks.length">
        <h4>Recently Visited</h4>
        <ul class="list-unstyled myuw-text-md">
          <uw-link
            v-for="(link, index) in recentLinks" :key="`recent-${index}`"
            :link="link" :buttons="['save']" :custom-id="`recent-${index}`"
          />
        </ul>
        <span>
          Save your recently visited links for future access.
        </span>
      </div>
      <hr v-if="recentLinks.length">
      <p class="m-0 myuw-text-md">
        <span>
          Not seeing the links you're looking for?
          <span v-if="popularLinks.length">
            Select from
            <b-button v-b-toggle.popular_qlinks variant="link" size="sm"
                      disabled class="d-inline-block align-bottom p-0 border-0"
            >
              popular links,
            </b-button>
            or
          </span>
          <b-button v-b-toggle.custom_qlinks variant="link" size="sm"
                    :disabled="disableActions"
                    class="d-inline-block align-bottom p-0 border-0"
          >
            Add your own.
          </b-button>
        </span>
      </p>

      <b-collapse id="popular_qlinks">
        <h4 class="h6 font-weight-bold">
          Popular Links
        </h4>
        <ul class="list-unstyled myuw-text-md">
          <uw-link
            v-for="(link, index) in popularLinks" :key="`popular-${index}`"
            :link="link" :buttons="['save']" :custom-id="`popular-${index}`"
          />
        </ul>
      </b-collapse>

      <b-collapse
        id="custom_qlinks"
        role="form"
        aria-labelledby="custom_qlinks_label"
        class="bg-light mx-n3 p-3 mt-3"
      >
        <b-form class="myuw-text-md" @submit="addLink" @reset="onReset">
          <h4 class="h6 font-weight-bold">
            Add your link to Quick Links
          </h4>
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
              <span>Error saving</span>
            </div>
            <div v-if="isAddFetching" id="quicklink_saving">
              <span>Saving...</span>
            </div>
          </div>
          <div class="d-flex justify-content-end">
            <b-button v-b-toggle.custom_qlinks
                      variant="link" type="reset" size="sm"
            >
              Cancel
            </b-button>
            <b-button variant="primary" type="submit" size="sm">
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
import Card from '../../../../containers/card.vue';
import Link from './link.vue';

export default {
  components: {
    'uw-card': Card,
    'uw-link': Link,
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
      recentLinks: (state) => state.value.recentLinks,
      popularLinks: (state) => state.value.popularLinks,
      customLinks: (state) => state.value.customLinks,
      defaultLinks: (state) => state.value.defaultLinks,
    }),
    ...mapGetters('quicklinks', {
      isReady: 'isReady',
      isErrored: 'isErrored',
      isAddFetching: 'isAddFetching',
      isAddErrored: 'isAddErrored',
    }),
  },
  methods: {
    ...mapActions('quicklinks', {
      quicklinksAddLink: 'addLink',
    }),
    addLink: function(event) {
      event.preventDefault();
      this.quicklinksAddLink(this.customLink);
    },
    onReset: function(event) {
      event.preventDefault();
      this.customLink = {};
    },
  },
};
</script>

<style lang="scss" scoped>
</style>
