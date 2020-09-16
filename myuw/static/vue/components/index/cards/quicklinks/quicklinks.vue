<template>
  <uw-card :loaded="true" :errored="false">
    <template #card-heading>
      <h3>Quick Links</h3>
    </template>
    <template #card-body>
      <ul class="quicklinks-list">
        <uw-link
          v-for="(link, index) in defaultLinks" :key="`default-${index}`"
          :link="link" :buttons="['remove']" :customId="`default-${index}`"
        />
        <uw-link
          v-for="(link, index) in customLinks" :key="`custom-${index}`"
          :link="link" :buttons="['edit', 'remove']"
          :customId="`custom-${index}`" canActuallyRemove
        />
      </ul>
      <hr />
      <div v-if="recentLinks.length">
        <h4>Recently Visited</h4>
        <ul class="quicklinks-list">
          <uw-link
            v-for="(link, index) in recentLinks" :key="`recent-${index}`"
            :link="link" :buttons="['save']" :customId="`recent-${index}`"
          />
        </ul>
        <span>
          Save your recently visited links for future access.
        </span>
      </div>
      <hr v-if="recentLinks.length" />
      <div>
        <span>
          Not seeing the links you're looking for?
          <span v-if="popularLinks.length">
            Select from
            <b-button v-b-toggle.popular_qlinks>
              popular links,
            </b-button>
            or
          </span>
          <b-button v-b-toggle.custom_qlinks :disabled="disableActions">
            add your own
          </b-button>.
        </span>
      </div>

      <b-collapse id="popular_qlinks">
        <h4>Popular Links</h4>
        <ul class="quicklinks-list">
          <uw-link
            v-for="(link, index) in popularLinks" :key="`popular-${index}`"
            :link="link" :buttons="['save']" :customId="`popular-${index}`"
          />
        </ul>
      </b-collapse>
      <b-collapse
        id="custom_qlinks"
        role="form"
        aria-labelledby="custom_qlinks_label"
      >
        <b-form @submit="addLink" @reset="onReset">
          <h4>Add your link to Quick Links</h4>
          <b-form-group label="URL" label-for="myuw-custom-qlink">
            <b-form-input
              type="url"
              id="myuw-custom-qlink"
              v-model="customLink.url"
              placeholder="https://www.washington.edu"
              required
            >
            </b-form-input>
          </b-form-group>
          <b-form-group label="Link name (optional)" label-for="myuw-custom-qlink-label">
            <b-form-input
              type="text"
              id="myuw-custom-qlink-label"
              v-model="customLink.label"
              placeholder="UW Homepage"
            >
            </b-form-input>
          </b-form-group>
          <div>
            <div id="error_saving" v-if="isAddErrored">
              <span>Error saving</span>
            </div>
            <div id="quicklink_saving" v-if="isAddFetching">
              <span>Saving...</span>
            </div>
          </div>
          <b-button type="reset" v-b-toggle.custom_qlinks>Cancel</b-button>
          <b-button type="submit">Add</b-button>
        </b-form>
      </b-collapse>
    </template>
  </uw-card>
</template>

<script>
import { mapGetters, mapState, mapActions } from "vuex";
import Card from "../../../../containers/card.vue";
import Link from "./link.vue";

export default {
  components: {
    "uw-card": Card,
    'uw-link': Link,
  },
  data: function () {
    return {
      customLink: {},
    };
  },
  computed: {
    ...mapState({
      disableActions: (state) => state.disableActions,
      user: (state) => state.user,
    }),
    ...mapState("quicklinks", {
      recentLinks: (state) => state.value.recentLinks,
      popularLinks: (state) => state.value.popularLinks,
      customLinks: (state) => state.value.customLinks,
      defaultLinks: (state) => state.value.defaultLinks,
    }),
    ...mapGetters("quicklinks", {
      isReady: "isReady",
      isErrored: "isErrored",
      isAddFetching: "isAddFetching",
      isAddErrored: "isAddErrored",
    }),
  },
  methods: {
    ...mapActions('quicklinks', {
      quicklinksAddLink: 'addLink',
      quicklinksUpdateLink: 'updateLink',
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
.quicklinks-list {
  list-style: none;
  padding-left: 0;
}
</style>
