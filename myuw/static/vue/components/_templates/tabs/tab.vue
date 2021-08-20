<template>
  <div ref="tab" class="tab-pane" role="tabpanel" aria-labelledby="todo" tabindex="0">
    <slot v-if="render" />
  </div>
</template>

<script>

export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    titleItemClass: {
      type: [String, Array, Object],
      default: '',
    },
    titleLinkClass: {
      type: [String, Array, Object],
      default: '',
    },
  },
  data() {
    return {
      render: false,
    };
  },
  mounted() {
    this.$set(this.$parent.actualTabs, this.$refs.tab.id, this);
    if (this.$refs.tab.classList.contains('active')) { this.render = true };
    var tabEl = document
      .querySelector(`button[data-bs-toggle="tab"][data-bs-target="#${this.$refs.tab.id}"]`);
    tabEl.addEventListener('show.bs.tab', (event) => {
      this.$nextTick(() => {
        if (!event.defaultPrevented) {
          this.render = true;
        }
      });
    });
  }
}
</script>