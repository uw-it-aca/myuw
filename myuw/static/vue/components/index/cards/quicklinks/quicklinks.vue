<template>
  <uw-card :loaded="true" :errored="false">
    <template #card-heading>
      <h3>Quick Links</h3>
    </template>
    <template #card-body>
      <ul>
        <uw-link
          v-for="(link, index) in defaultLinks" :key="index"
          :link="link" :buttons="['remove']"
        />
        <uw-link
          v-for="(link, index) in customLinks" :key="index"
          :link="link" :buttons="['edit', 'remove']"
        />
      </ul>
      <hr />
      <div v-if="recentLinks.length">
        <h4>Recently Visited</h4>
        <ul>
          <uw-link
            v-for="(link, index) in recentLinks" :key="index"
            :link="link" :buttons="['save']"
          />
        </ul>
        <span>
          Save your recently visited links for future access.
        </span>
      </div>
      <hr v-if="recentLinks.length" />
      <b-collapse id="custom-link-edit">
        <b-form @submit="saveLink">
          <h4>Edit Quick Link</h4>
          <b-form-group label="URL" label-for="custom-link-edit-url">
            <b-form-input type="url" id="custom-link-edit-url" v-model="custom_link.url" required>
            </b-form-input>
          </b-form-group>
          <b-form-group label="Link name (optional)" label-for="custom-link-edit-label">
            <b-form-input type="url" id="custom-link-edit-label" v-model="custom_link.label">
            </b-form-input>
          </b-form-group>
          <b-button type="reset">Cancel</b-button>
          <b-button type="submit">Save</b-button>
        </b-form>
        <div class="form">
          <fieldset>
            
            <input type="hidden" id="custom-link-edit-id" />
            <div style="padding: 8px 0;">
              
            </div>
          </fieldset>
        </div>
      </b-collapse>
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
        <ul>
          <uw-link
            v-for="(link, index) in popularLinks" :key="index"
            :link="link" :buttons="['save']"
          />
        </ul>
      </b-collapse>
      <b-collapse
        id="custom_qlinks"
        role="form"
        aria-labelledby="custom_qlinks_label"
      >
        <div>
          <h4 id="custom_qlinks_label">Add your link to Quick Links</h4>
          <div>
            <label for="myuw-custom-qlink" class="sr-only">Web Address</label>
            <fieldset>
              <label for="myuw-custom-qlink">URL</label>
              <input
                type="url"
                placeholder="https://www.washington.edu"
                id="myuw-custom-qlink"
                value=""
              />
              <br />
              <label for="myuw-custom-qlink-label">
                Link name (optional)
              </label>
              <input
                type="text"
                placeholder="UW Homepage"
                id="myuw-custom-qlink-label"
                value=""
              />
              <br />
              <div>
                <div>
                  <div>
                    <a data-toggle="collapse" href="#custom_qlinks">Cancel</a>
                    <button id="quicklinks-save-new">
                      Add
                    </button>
                  </div>
                </div>
                <div id="error_saving">
                  <span>Error saving</span>
                </div>
                <div id="quicklink_saving">
                  <span>Saving...</span>
                </div>
              </div>
            </fieldset>
          </div>
        </div>
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
      custom_link: {},
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
    }),
  },
  methods: {
    removeLink(link) {

    }
  },
};
</script>

<style scoped></style>
