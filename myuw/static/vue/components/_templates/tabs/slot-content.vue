<script>
export default {
  props: {
    node: {
      type: Array,
      required: true,
    },
  },
  render(createElement) {
    console.log(this.node);
    return createElement('div', this.node);
  },
}
</script>