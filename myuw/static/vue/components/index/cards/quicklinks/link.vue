<template>
  <li class="quicklinks-link">
    <a :href="link.url" :title="link.label" target="_blank">
      <span>{{ link.label }}</span>
    </a>
    <b-button
      v-if="activeButtons['edit']" variant="link"
      :title="`Edit ${link.label} link`"
      v-b-toggle="`${customId}-collapse`"
    >
      <font-awesome-icon :icon="['fas', 'pencil-alt']" />
    </b-button>
    <b-button
      v-if="activeButtons['remove']" variant="link"
      :title="`Remove ${link.label} link from Quick Links list`"
      @click="removeLink({link, canActuallyRemove})"
    >
      <font-awesome-icon :icon="['fas', 'times']" />
    </b-button>
    <div v-if="activeButtons['save']">
      <font-awesome-icon
        v-if="link.added"
        :title="`${link.label} link saved to Quick Links`"
        :icon="['fa', 'check']"
      />
      <b-button
        v-else variant="link"
        :title="`Save ${link.label} link to your Quick Links list`"
        @click="saveLink(link)"
      >
        <font-awesome-icon :icon="['fas', 'plus']" />
      </b-button>
    </div>
    <b-collapse v-if="activeButtons['edit']" :id="`${customId}-collapse`">
      <b-form @submit="updateLink" @reset="onReset">
        <h4>Edit Quick Link</h4>
        <b-form-group label="URL" :label-for="`${customId}-edit-url`">
          <b-form-input type="url" :id="`${customId}-edit-url`" v-model="currentCustomLink.url" required>
          </b-form-input>
        </b-form-group>
        <b-form-group label="Link name (optional)" :label-for="`${customId}-edit-label`">
          <b-form-input type="text" :id="`${customId}-edit-label`" v-model="currentCustomLink.label">
          </b-form-input>
        </b-form-group>
        <b-button type="reset" v-b-toggle="`${customId}-collapse`">Cancel</b-button>
        <b-button type="submit">Save</b-button>
      </b-form>
    </b-collapse>
  </li>
</template>

<script>
import { mapActions } from "vuex";

export default {
  props: {
    link: {
      type: Object,
      required: true,
    },
    buttons: {
      type: Array,
      default: [],
    },
    customId: {
      type: String,
      required: true,
    },
    canActuallyRemove: {
      type: Boolean,
      default: false,
    },
  },
  data: function() {
    return {
      activeButtons: {
        edit: false,
        remove: false,
        save: false,
      },
      currentCustomLink: {},
    } 
  },
  created() {
    this.buttons.forEach((button) => {
      this.activeButtons[button] = true;
    });

    // Create a deep clone
    this.currentCustomLink = JSON.parse(JSON.stringify(this.link));
  },
  methods: {
    ...mapActions('quicklinks', {
      removeLink: 'removeLink',
      quicklinksUpdateLink: 'updateLink',
    }),
    addLink: function(event) {
      event.preventDefault();
      this.quicklinksAddLink(this.customLink);
    },
    updateLink: function(event) {
      event.preventDefault();
      this.quicklinksUpdateLink(this.currentCustomLink);
    },
    onReset: function(event) {
      event.preventDefault();
      this.currentCustomLink = {};
      this.customLink = {};
    },
    saveLink() {

    },
  }
}
</script>

<style lang="scss" scoped>
.quicklinks-link {
  button {
    padding: 0;
  }
}
</style>