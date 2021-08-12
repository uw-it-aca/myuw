<template>
  <li class="mb-1 myuw-quicklinks">
    <div class="d-flex">
      <a :href="link.url" class="me-auto pe-1">
        {{ link.label }}
      </a>
      <span v-if="!isEditOpen">
        <button v-if="activeButtons['edit']"
          v-uw-collapse="`${customId}-collapse`"
          type="button"
          :aria-label="`Edit link '${link.label}'`"
          title="Edit link"
          class="btn btn-link btn-sm p-0 me-1 border-0 align-bottom"
          :class="[$mq === 'mobile' ? 'text-muted' : 'text-white']"
        >
          <font-awesome-icon :icon="faPencilAlt" />
        </button>
        <button v-if="activeButtons['remove']"
          type="button"
          :aria-label="`Remove link '${link.label}' from Quick Links list`"
          title="Remove link from Quick Links list"
          class="btn btn-link btn-sm p-0 m-0 border-0 align-bottom"
          :class="[$mq === 'mobile' ? 'text-muted' : 'text-white']"
          @click="removeLink(link, canActuallyRemove)"
        >
          <font-awesome-icon :icon="faTimes" />
        </button>
        <span v-if="activeButtons['save']">
          <font-awesome-icon
            v-if="link.added"
            :aria-label="`'${link.label}' saved to Quick Links`"
            title="Saved to Quick Links"
            :icon="faCheck"
            class="p-0 m-0 border-0 align-bottom"
            :class="[$mq === 'mobile' ? 'text-muted' : 'text-light']"
            size="sm"
          />
          <button v-else
            type="button"
            :aria-label="`Save link '${link.label}' to your Quick Links list`"
            title="Save link to your Quick Links list"
            class="btn btn-link btn-sm p-0 m-0 border-0 align-bottom"
            :class="[$mq === 'mobile' ? 'text-muted' : 'text-light']"
            @click="saveLink"
          >
            <font-awesome-icon :icon="faPlus" />
          </button>
        </span>
      </span>
    </div>

    <uw-collapse
      v-if="activeButtons['edit']"
      :id="`${customId}-collapse`"
      v-model="isEditOpen"
      class="bg-light mx-n3 p-3 my-1"
      @open="populateCustomLink"
    >
      <form @submit="updateLink" @reset="onReset">
        <h3 class="h6 fw-bold">
          Edit Quick Link
        </h3>
        <div class="mb-3">
          <label :for="`${customId}-edit-url`" class="form-label">
            URL
          </label>
          <input
            :id="`${customId}-edit-url`"
            v-model="currentCustomLink.url"
            class="form-control"
            type="url"
            required
            size="sm"
          />
        </div>
        <div class="mb-3">
          <label :for="`${customId}-edit-label`" class="form-label">
            Link name (optional)
          </label>
          <input
            :id="`${customId}-edit-label`"
            v-model="currentCustomLink.label"
            class="form-control"
            type="text"
            size="sm"
          />
        </div>
        <div class="d-flex justify-content-end">
          <button v-uw-collapse="`${customId}-collapse`" class="btn btn-link btn-sm"
            type="reset"
          >Cancel</button>
          <button class="btn btn-primary btn-sm" type="submit"
          >Save</button>
        </div>
      </form>
    </uw-collapse>
  </li>
</template>

<script>
import {
  faTimes,
  faPencilAlt,
  faCheck,
  faPlus,
} from '@fortawesome/free-solid-svg-icons';
import {mapActions} from 'vuex';
import Collapse from '../../_templates/collapse.vue';

export default {
  components: {
    'uw-collapse': Collapse,
  },
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
      faTimes,
      faPencilAlt,
      faCheck,
      faPlus,
    };
  },
  created() {
    this.buttons.forEach((button) => {
      this.activeButtons[button] = true;
    });

    this.populateCustomLink();
  },
  methods: {
    ...mapActions('quicklinks', {
      addLink: 'addLink',
      quicklinksRemoveLink: 'removeLink',
      quicklinksUpdateLink: 'updateLink',
    }),
    removeLink(link, canActuallyRemove) {
      this.$logger.quicklink('remove', link.url);
      this.quicklinksRemoveLink({link, canActuallyRemove});
    },
    updateLink: function(event) {
      event.preventDefault();
      this.$logger.quicklink('edit', this.currentCustomLink.url);
      this.quicklinksUpdateLink(this.currentCustomLink);
      this.isEditOpen = false;
    },
    onReset: function(event) {
      event.preventDefault();
      this.populateCustomLink();
      this.isEditOpen = false;
    },
    saveLink(event) {
      event.preventDefault();
      this.$logger.quicklink('add', this.link.url);
      this.addLink(this.link);
    },
    populateCustomLink() {
      this.currentCustomLink = JSON.parse(JSON.stringify(this.link));
    }
  },
};
</script>

<style lang="scss" scoped>
@use "sass:map";
@import "../../../../css/myuw/variables.scss";

.myuw-quicklinks {
  &:focus,
  &:focus-within,
  &:hover {
    //handle visibility of remove/edit buttons
    button.text-white,
    button.text-light,
    svg.text-light {
      color: $text-muted !important;
    }
  }
}
</style>
