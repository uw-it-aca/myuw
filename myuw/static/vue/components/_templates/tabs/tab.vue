<template>
  <div ref="tab" class="tab-pane fade" role="tabpanel" aria-labelledby="todo">
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
    let setRenderTrue = () => { this.render = true; }
    tabEl.addEventListener('show.bs.tab', function (_event) {
      setRenderTrue();
    });
  }
}
</script>