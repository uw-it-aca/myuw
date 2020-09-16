<template>
  <li class="quicklinks-link">
    <a :href="link.url" :title="link.label" target="_blank">
      <span>{{ link.label }}</span>
    </a>
    <b-button
      v-if="activeButtons['edit']" variant="link"
      :title="`Edit ${link.label} link`"
      v-b-toggle="editId" @click="updateCustomCurrent(link)"
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
    editId: {
      type: String,
      default: null,
    },
    canActuallyRemove: {
      type: Boolean,
      default: false,
    },
    updateCustomCurrent: {
      type: Function,
    }
  },
  data: function() {
    return {
      activeButtons: {
        edit: false,
        remove: false,
        save: false,
      }
    } 
  },
  created() {
    this.buttons.forEach((button) => {
      this.activeButtons[button] = true;
    });
  },
  methods: {
    ...mapActions('quicklinks', ['removeLink',]),
    editLink() {

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