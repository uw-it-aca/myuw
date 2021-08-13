<template>
  <li class="nav-item" :class="titleItemClass" role="presentation">
    <button
      class="nav-link text-nowrap text-uppercase"
      :class="titleLinkClass"
      data-bs-toggle="tab"
      data-bs-target="#home"
      type="button"
      role="tab"
      aria-controls="home"
      aria-selected="true"
    >
      <slot name="title">{{title}}</slot>
    </button>
  </li>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    titleItemClass: {
      type: String,
      default: '',
    },
    titleLinkClass: {
      type: String,
      default: '',
    },
  },
  mounted() {
    this.$parent.ready.push(true);
  }
}
</script>