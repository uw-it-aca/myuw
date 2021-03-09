<template>
  <a ref="link" :href="href" :title="title" @click="onClick">
    <slot />
  </a>
</template>

<script>
export default {
  functional: true,
  props: {
    href: {
      type: String,
      required: true,
    },
    out: {
      type: Boolean,
      default: false,
    },
    outLabel: {
      type: String,
      default: null,
    },
    title: {
      type: String,
      default: null,
    },
  },
  methods: {
    onClick(evt) {
      let nav = {
        out: false,
      }; 
      if (this.out || this.outLabel) {
        nav.out = true;
        evt.preventDefault();
        let label = this.outLabel ? this.outLabel : this.title;
        if (!label) {
          console.log(this.$refs.link);
          label = this.$refs.link.text;
        }
        nav.label = label;
        label = encodeURIComponent(label);
        const encodedHref = encodeURIComponent(this.href);
        nav.location = `${document.location.origin}/out?u=${encodedHref}&l=${lable}`;
      } else {
        console.log(this.$refs.link.text);
        nav.label = this.title ? this.title : this.$refs.link.text;
        nav.location = this.href;
      }
      this.$logger.linkClick(this, this.href, nav.label, nav.out);
      window.location = nav.location;
    }
  }
}
</script>