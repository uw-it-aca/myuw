<template>
  <li class="mb-1 myuw-quicklinks">
    <div class="d-flex">
      <a :href="link.url" :title="link.label"
         target="_blank" class="mr-auto pr-1"
      >
        {{ link.label }}
      </a>
      <span v-if="!isEditOpen">
        <b-button
          v-if="activeButtons['edit']" v-b-toggle="`${customId}-collapse`"
          variant="link"
          :title="`Edit ${link.label} link`"
          class="p-0 m-0 border-0 align-bottom text-white"
          size="sm"
        >
          <font-awesome-icon :icon="['fas', 'pencil-alt']" />
        </b-button>
        <b-button
          v-if="activeButtons['remove']" variant="link"
          :title="`Remove ${link.label} link from Quick Links list`"
          class="p-0 m-0 border-0 align-bottom text-white"
          size="sm"
          @click="removeLink({link, canActuallyRemove})"
        >
          <font-awesome-icon :icon="['fas', 'times']" />
        </b-button>
        <span v-if="activeButtons['save']">
          <font-awesome-icon
            v-if="link.added"
            :title="`${link.label} link saved to Quick Links`"
            :icon="['fa', 'check']"
            class="p-0 m-0 border-0 align-bottom text-light"
            size="sm"
          />
          <b-button
            v-else variant="link"
            :title="`Save ${link.label} link to your Quick Links list`"
            class="p-0 m-0 border-0 align-bottom text-light"
            size="sm"
            @click="saveLink"
          >
            <font-awesome-icon :icon="['fas', 'plus']" />
          </b-button>
        </span>
      </span>
    </div>

    <b-collapse
      v-if="activeButtons['edit']"
      :id="`${customId}-collapse`"
      v-model="isEditOpen"
      class="bg-light mx-n3 p-3 my-1"
    >
      <b-form @submit="updateLink" @reset="onReset">
        <h4 class="h6 font-weight-bold">
          Edit Quick Link
        </h4>
        <b-form-group label="URL" :label-for="`${customId}-edit-url`">
          <b-form-input
            :id="`${customId}-edit-url`"
            v-model="currentCustomLink.url"
            type="url" required
            size="sm"
          />
        </b-form-group>
        <b-form-group
          label="Link name (optional)"
          :label-for="`${customId}-edit-label`"
        >
          <b-form-input
            :id="`${customId}-edit-label`"
            v-model="currentCustomLink.label"
            type="text"
            size="sm"
          />
        </b-form-group>
        <div class="d-flex justify-content-end">
          <b-button v-b-toggle="`${customId}-collapse`"
                    variant="link" size="sm" type="reset"
          >
            Cancel
          </b-button>
          <b-button variant="primary" size="sm" type="submit">
            Save
          </b-button>
        </div>
      </b-form>
    </b-collapse>
  </li>
</template>

<script>
import {mapActions} from 'vuex';

export default {
  props: {
    link: {
      type: Object,
      required: true,
    },
    buttons: {
      type: Array,
      default: () => [],
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
      isEditOpen: false,
    };
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
      addLink: 'addLink',
      removeLink: 'removeLink',
      quicklinksUpdateLink: 'updateLink',
    }),
    updateLink: function(event) {
      event.preventDefault();
      this.quicklinksUpdateLink(this.currentCustomLink);
      this.onReset({preventDefault: () => {}});
    },
    onReset: function(event) {
      event.preventDefault();
      this.currentCustomLink = JSON.parse(JSON.stringify(this.link));
      this.isEditOpen = false;
    },
    saveLink(event) {
      event.preventDefault();
      this.addLink(this.link);
    },
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../../css/myuw/variables.scss";

.myuw-quicklinks {
  &:focus, &:focus-within, &:hover {
    //handle visibility of remove/edit buttons
    button.text-white, button.text-light, svg.text-light {
      color: $text-muted !important;
    }
  }
}

</style>
